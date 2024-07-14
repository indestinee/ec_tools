import dataclasses
import logging
import time
import unittest
from typing import List

from ec_tools.database import SqliteDataObject, SqliteClient, SqliteDao

logging.basicConfig(level=logging.DEBUG)


@dataclasses.dataclass
class Fruit(SqliteDataObject):
    name: str
    weight: float
    price: float
    is_delicious: bool
    remaining: int

    @classmethod
    def primary_keys(cls) -> List[str]:
        return ["name", "is_delicious"]

    @classmethod
    def extra_indexes(cls) -> List[List[str]]:
        return [["is_delicious", "price"], ["is_delicious", "weight"]]


class SqliteDaoTest(unittest.TestCase):
    sqlite_client = SqliteClient(":memory:")
    sqlite_dao = SqliteDao[Fruit](sqlite_client, Fruit)

    def test(self):
        logging.info("dao: %s", self.sqlite_dao)
        self.sqlite_dao.drop_table()
        self.sqlite_dao.create_table()
        result = self.sqlite_dao.insert(
            [
                Fruit(
                    name="apple", weight=1.1, price=1, is_delicious=True, remaining=1
                ),
                Fruit(
                    name="banana", weight=0.1, price=0, is_delicious=False, remaining=0
                ),
            ]
        )
        logging.info("insert result: %s", result)
        apple = self.sqlite_dao.query_by_values(1, 0)[0]
        banana = self.sqlite_dao.query_by_values(1, 1)[0]
        banana_1 = self.sqlite_dao.query_by_values(1, 0, name="banana")[0]
        self.assertEqual(self.sqlite_dao.count_by_values(), 2)
        self.assertEqual(self.sqlite_dao.count_by_values(name="apple"), 1)
        self.assertEqual(
            self.sqlite_dao.count_group_by_values(group_by=["name"]),
            [{"name": "apple", "count": 1}, {"name": "banana", "count": 1}],
        )
        self.assertEqual(
            self.sqlite_dao.count_group_by_values(group_by=["name", "is_delicious"]),
            [
                {"count": 1, "is_delicious": 1, "name": "apple"},
                {"count": 1, "is_delicious": 0, "name": "banana"},
            ],
        )

        self.assertEqual(banana, banana_1)
        self.assertEqual(apple.name, "apple")
        self.assertEqual(
            self.sqlite_dao.query_fields_by_values(fields=["name"]),
            [{"name": "apple"}, {"name": "banana"}],
        )
        self.assertEqual(apple.weight, 1.1)
        self.assertEqual(apple.remaining, 1)
        self.assertEqual(apple.is_delicious, True)
        self.assertIsNotNone(apple.created_at)
        self.assertIsNotNone(apple.updated_at)
        created_at = apple.created_at
        self.sqlite_dao.insert_or_replace([apple])
        apple = self.sqlite_dao.query_by_values(1, 1)[0]
        self.assertEqual(apple.name, "apple")
        self.assertEqual(apple.created_at, created_at)
        self.assertEqual(banana.name, "banana")
        self.assertEqual(banana.weight, 0.1)
        self.assertEqual(banana.remaining, 0)
        self.assertEqual(banana.is_delicious, False)
        self.assertIsNotNone(banana.created_at)
        self.sqlite_dao.delete_by_values(name="apple", is_delicious=None)
        self.assertEqual(self.sqlite_dao.query_by_values(1, 0, name="apple"), [])
        self.assertEqual(self.sqlite_dao.query_by_values(1, 0), [banana])
        self.assertRaises(
            AssertionError,
            lambda: self.sqlite_dao.query_by_values(1, 0, sql_inject_field="123"),
        )
        self.sqlite_dao.delete_by_values()
        self.assertEqual(self.sqlite_dao.query_by_values(1, 0), [])

    def test_obj(self):
        created_at = time.time()
        fruit_json = Fruit.from_json(
            {
                "name": "apple",
                "weight": 1.0,
                "price": 1.0,
                "is_delicious": "True",
                "remaining": 1,
                "created_at": created_at,
                "updated_at": created_at,
            }
        )
        fruit_obj = Fruit(
            name="apple",
            weight=1.0,
            price=1.0,
            is_delicious=True,
            remaining=1,
            created_at=created_at,
            updated_at=created_at,
        )
        logging.info("fruit_json: %s", fruit_json)
        logging.info("fruit_obj: %s", fruit_obj)
        self.assertEqual(fruit_obj, fruit_json)

        logging.info("fruit_json: %s", fruit_json.to_json())
