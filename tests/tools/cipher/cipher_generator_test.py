import logging
import time
import os
import unittest

from ec_tools.tools.cipher import AesCipherGenerator, Cipher, CipherGenerator, AesMode

logging.basicConfig(level=logging.DEBUG)


class CipherGeneratorTest(unittest.TestCase):
    def test(self):
        for mode in AesMode:
            cipher_generator: CipherGenerator = AesCipherGenerator(mode=mode)
            for length in list(range(32)) + [127, 256]:
                password = os.urandom(length)
                plain_text = os.urandom(length)
                cipher = cipher_generator.encrypt(password, plain_text)
                self.assertTrue(cipher.mode.startswith("AES_"))
                self.assertEqual(plain_text, cipher_generator.decrypt(password, cipher))
