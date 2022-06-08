import unittest

import Lambda


class VersionTestCase(unittest.TestCase):
    """ Version tests """

    def test_version(self):
        """ check Lambda exposes a version attribute """
        self.assertTrue(hasattr(Lambda, "__version__"))
        self.assertIsInstance(Lambda.__version__, str)


if __name__ == "__main__":
    unittest.main()
