import unittest

from ec_tools import procedure


class TestProcedure(unittest.TestCase):
    def test_str(self):
        with procedure('hi') as p:
            p.add_log('(#r)hi hi hi')


if __name__ == '__main__':
    unittest.main()
