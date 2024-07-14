import dataclasses
import enum
import json
import unittest
from typing import List

from ec_tools.data import DataObject


@dataclasses.dataclass
class SeaAnimalInfo(DataObject):
    name: str


class SeaAnimalType(enum.Enum):
    FISH = SeaAnimalInfo("fish")
    SHRIMP = SeaAnimalInfo("shrimp")


@dataclasses.dataclass
class Sea(DataObject):
    animals: List[SeaAnimalType]


class DataObjectEnumTest(unittest.TestCase):
    def test_enums(self):
        a = Sea([SeaAnimalType.FISH, SeaAnimalType.SHRIMP])
        a_json = a.to_json()
        aa = Sea.from_json(a_json)
        self.assertEqual({"animals": ["FISH", "SHRIMP"]}, a_json)
        self.assertEqual(a, aa)
