import dataclasses
import unittest
from typing import List, Dict, Optional, Set

from ec_tools.data import DataObject


@dataclasses.dataclass
class Human(DataObject):
    name: str
    nick_name: Optional[str] = dataclasses.field(default=None)
    gender: Optional[str] = None
    age: int = 20


@dataclasses.dataclass
class School(DataObject):
    students: List[List[Human]]
    students_set: Set[int]
    students_by_classes: Dict[str, Human]
    student_representative: Optional[Human]


class DataObjectComplexTest(unittest.TestCase):
    def test_deserialize_human(self):
        human_json = {"name": "a", "nick_name": None}
        human = Human.from_json(human_json)
        self.assertEqual(Human("a", nick_name=None, gender=None, age=20), human)

    def test(self):
        stu1 = Human("a1")
        stu2 = Human("a2")
        school = School(
            students=[[stu1, stu2]],
            students_set={1, 2},
            students_by_classes={"1": stu1, "2": stu2},
            student_representative=stu1,
        )
        json_school = {
            "students": [[{"name": "a1", "nickname": None}, {"name": "a2"}]],
            "students_set": {1, 2},
            "students_by_classes": {"1": {"name": "a1"}, "2": {"name": "a2"}},
            "student_representative": {"name": "a1"},
        }
        school1 = School.from_json(json_school)
        self.assertEqual(school, school1)
