import unittest
import os

from ec_tools import ColorfulLog


class TestColorfulLog(unittest.TestCase):
    def test_log(self):
        log = ColorfulLog()
        self.assertTrue(os.path.isfile(log.log_path))
        log.error('hi')
        with open(log.log_path) as f:
            log_text = f.read()
            self.assertTrue('hi' in log_text)
            self.assertTrue('(#' not in log_text)


if __name__ == '__main__':
    unittest.main()
