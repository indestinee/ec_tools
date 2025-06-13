import os
import unittest

from ec_tools.utils import io_utils


class IoTest(unittest.TestCase):
    def test_load_json(self):
        self.assertEqual(
            {"a": "b"},
            io_utils.load_json(os.path.join(os.path.dirname(__file__), "test.json")),
        )
        self.assertEqual(
            {},
            io_utils.load_json(
                os.path.join(os.path.dirname(__file__), "test_not_exist.json"), {}
            ),
        )
        self.assertRaises(
            IOError,
            lambda: io_utils.load_json(
                os.path.join(os.path.dirname(__file__), "test_not_exist.json")
            ),
        )


if __name__ == "__main__":
    unittest.main()
