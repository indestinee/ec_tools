import unittest

from ec_tools import colorful_str


class TestColorfulStr(unittest.TestCase):
    def test_str(self):
        self.assertEqual('\033[1;31mhello hi\033[1;0m',
                         colorful_str('(#r)hello', 'hi'))
        self.assertEqual('\033[1;34mhello\033[1;0m', colorful_str('(#b)hello'))
        self.assertEqual('\033[1;34mhi ok\033[1;0m',
                         colorful_str.blue('hi', 'ok'))


if __name__ == '__main__':
    unittest.main()
