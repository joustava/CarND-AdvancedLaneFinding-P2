
import unittest
# ignoring error as pylint nags as it doesn't know about editable local installs?
from tlc import classifier  # pylint: disable=import-error


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(classifier.fun(1), 3)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
