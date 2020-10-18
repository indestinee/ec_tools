import unittest
from ec_tools import ReplaceDict


class TestReplaceDict(unittest.TestCase):
    def test_replace(self):
        replace_dict = ReplaceDict(rep_dict={
            'hi': '123',
            'hello': '456',
            'help': '9'
        })
        self.assertEqual(
            '123, 456 world, hai hel 9.',
            replace_dict.replace('hi, hello world, hai hel help.'),
        )


if __name__ == '__main__':
    unittest.main()
