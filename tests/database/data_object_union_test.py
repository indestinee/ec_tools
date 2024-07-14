import dataclasses
import unittest
from typing import List, Dict, Union, Any

from ec_tools.data import DataObject


@dataclasses.dataclass
class A(DataObject):
    x: int
    y: Union[int, str]


@dataclasses.dataclass
class B(DataObject):
    a: List[Dict[str, A]]


@dataclasses.dataclass
class C(DataObject):
    x: int
    y: Union[int, str]

    @classmethod
    def _load__y(cls, value: Any):
        if isinstance(value, int):
            return int(value)
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return str(value)


@dataclasses.dataclass
class D(DataObject):
    c: List[Dict[str, C]]


class DataObjectUnionTest(unittest.TestCase):
    def test(self):
        b_json = {"a": [{"1": {"x": 1, "y": "2"}}]}
        with self.assertRaises(Exception) as e:
            B.from_json(b_json)
            self.assertTrue(
                'A#y is not serializable, try to add function "_load__y" with "@classmethod" to A'
                in e
            )

    def test_load(self):
        d_json = {"c": [{"1": {"x": 1, "y": "2"}}]}
        d = D([{"1": C(1, 2)}])
        self.assertEqual(d, D.from_json(d_json))
