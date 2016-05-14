import unittest
from core import rsa


class Testrsa(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(rsa.gcd(6, 3), 3)
        self.assertEqual(rsa.gcd(128, 7), 1)
        self.assertEqual(rsa.gcd(-10, 11), 1)

    def test_pow_mod(self):
        self.assertEqual(rsa.power_mod(2, 3, 7), 1)
        self.assertEqual(rsa.power_mod(3, 2, 3), 0)
        with self.assertRaises(TypeError):
            self.assertEqual(rsa.power_mod(2, 0.5, 7), 0)

    def test_prime_test(self):
        self.assertTrue(rsa.prime_test(4567))
        self.assertTrue(rsa.prime_test(7))
        self.assertTrue(rsa.prime_test(997))
        self.assertFalse(rsa.prime_test(4))
        self.assertFalse(rsa.prime_test(4666))

    def test_all(self):
        result = []
        key = rsa.key_generator()
        mssg = "Hello world!"
        mssg = rsa.text_to_ascii(mssg)
        mssg = rsa.encryption(mssg, key['P'][0], key['P'][1])
        mssg = rsa.decryption(mssg, key['S'][0], key['S'][1])
        for _ in mssg:
            result.append(chr(_))
        result = "".join(result)
        self.assertEqual(result, "Hello world!")

if __name__ == "__main__":
    unittest.main()
