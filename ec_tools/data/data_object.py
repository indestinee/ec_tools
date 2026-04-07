import dataclasses
import enum
import json
from typing import Any, Callable, Dict, List, Set, get_args, get_origin


class CustomizedJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, enum.Enum):
            return o.name
        return json.JSONEncoder.default(self, o)


@dataclasses.dataclass
class FormatErrorException(Exception):
    class_name: str
    field: dataclasses.Field
    message: str

    def __repr__(self):
        return (
            f"{self.message}: {self.class_name}#{self.field.name} is not serializable, "
            f'try to add function "_load__{self.field.name}" with '
            f'"@classmethod" to {self.class_name}'
        )

    def __str__(self):
        return self.__repr__()


@dataclasses.dataclass
class Formatter:
    class_name: str
    field: dataclasses.Field

    def format_field(self, value: Any):
        value = self._get_value(value)
        if value is None:
            return value
        return self._format(self.field.type, value)

    def _format(self, field_type, value: Any):
        if field_type and isinstance(field_type, type):
            return self._format_by_class(field_type, value)
        return self._format_by_field(field_type, value)

    def _format_by_field(self, field_type, value: Any):
        if field_type.__dict__.get("_name", None) == "Optional":
            return self._format(get_args(field_type)[0], value)
        if get_origin(field_type) in [list, List]:
            return [self._format(get_args(field_type)[0], each) for each in value]
        if get_origin(field_type) in [set, Set]:
            return {self._format(get_args(field_type)[0], each) for each in value}
        if get_origin(field_type) in [dict, Dict]:
            return {
                self._format(get_args(field_type)[0], k): self._format(get_args(field_type)[1], v)
                for k, v in value.items()
            }
        raise FormatErrorException(self.class_name, self.field, f"unknown field type {field_type} to format")

    def _format_by_class(self, clazz: type, value: Any):
        if clazz is int:
            return int(value)
        if clazz is str:
            return str(value)
        if clazz is float:
            return float(value)
        if clazz is bool:
            if isinstance(value, str):
                if value.lower() == "true" or value == "1":
                    return True
                if value.lower() == "false" or value == "0":
                    return False
            return bool(value)
        if issubclass(clazz, DataObject):
            return clazz.from_json(value)
        if issubclass(clazz, enum.Enum):
            for each in clazz:
                if each.name == value:
                    return each
            raise FormatErrorException(
                self.class_name,
                self.field,
                f"unknown value {value} found in enum {clazz}",
            )
        raise FormatErrorException(self.class_name, self.field, f"unknown type {clazz} to format")

    def _get_value(self, value: Any):
        if value is not None:
            return value
        if self.field and self.field.default_factory != dataclasses.MISSING:
            return self.field.default_factory()
        if self.field and self.field.default != dataclasses.MISSING:
            return self.field.default
        return None


@dataclasses.dataclass
class DataObject:
    def __getitem__(self, key: str):
        return self.__dict__.get(key)

    def __setitem__(self, key: str, value: Any):
        self.__dict__[key] = value

    @classmethod
    def field_map(cls) -> Dict[str, dataclasses.Field]:
        return {field.name: field for field in cls.fields()}

    @classmethod
    def fields(cls) -> List[dataclasses.Field]:
        return list(dataclasses.fields(cls))

    @classmethod
    def field_names(cls) -> List[str]:
        return [field.name for field in dataclasses.fields(cls)]

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]):
        function_mapping = cls._customized_load_function("_load__")
        return cls(
            **{field.name: function_mapping[field.name](json_obj.get(field.name, None)) for field in cls.fields()}
        )

    def to_json(self) -> Dict[str, Any]:
        function_mapping = self._customized_dump_function("_dump__")
        return {
            field.name: (
                function_mapping[field.name](self.__dict__[field.name])
                if function_mapping[field.name]
                else json.loads(
                    json.dumps(dataclasses._asdict_inner(self.__dict__[field.name], dict), cls=CustomizedJsonEncoder)
                )
            )
            for field in self.fields()
        }

    def to_json_str(self) -> str:
        return json.dumps(self.to_json(), ensure_ascii=False, cls=CustomizedJsonEncoder)

    @classmethod
    def _customized_load_function(cls, prefix: str) -> Dict[str, Callable[[Any], Any]]:
        all_functions = {
            item: getattr(cls, item)
            for item in dir(cls)
            if isinstance(getattr(cls, item), Callable) and item.startswith(prefix)
        }
        return {
            field.name: all_functions.get(
                prefix + field.name,
                Formatter(class_name=cls.__name__, field=field).format_field,
            )
            for field in cls.fields()
        }

    @classmethod
    def _customized_dump_function(
        cls,
        prefix: str,
    ) -> Dict[str, Callable[[Any], Any]]:
        all_functions = {
            item: getattr(cls, item)
            for item in dir(cls)
            if isinstance(getattr(cls, item), Callable) and item.startswith(prefix)
        }
        return {field.name: all_functions.get(prefix + field.name) for field in cls.fields()}
