import unittest

from cyclomatic_complexity import Util


class Test(unittest.TestCase):
    def test_get_cyclomatic_complexity(self):
        util = Util()
        cc = util.get_cyclomatic_complexity("tests/python.py")
        self.assertEqual(cc, 2)

        cc = util.get_cyclomatic_complexity("tests/go.go")
        self.assertEqual(cc, 5)

        cc = util.get_cyclomatic_complexity("tests/js.js")
        self.assertEqual(cc, 3)


if __name__ == '__main__':
    unittest.main()
