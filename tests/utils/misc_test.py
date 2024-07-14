import logging
import os
import unittest

from ec_tools.utils import misc


class MiscTest(unittest.TestCase):
    test_log = os.urandom(12).hex() + "_test.log"

    def test_logger(self):
        assert not os.path.exists(self.test_log)
        logger = misc.get_logger(level=logging.DEBUG, fp=self.test_log)
        logger.info("hi")
        assert os.path.exists(self.test_log)
        with open(self.test_log, "r") as f:
            assert "hi" in f.read()
        if os.path.exists(self.test_log):
            os.remove(self.test_log)

    def __del__(self):
        if os.path.exists(self.test_log):
            os.remove(self.test_log)


if __name__ == "__main__":
    unittest.main()
