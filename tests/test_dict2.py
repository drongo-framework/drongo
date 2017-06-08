from drongo.utils import dict2

import unittest


class TestDict2(unittest.TestCase):
    def test_get_set(self):
        d = dict2()
        d.a = 100
        self.assertEqual(d.a, 100)
        d.b.a = 100
        self.assertEqual(d.b.a, 100)

    def test_conversion(self):
        a = {'a': ['b', 10, 20]}
        b = dict2.from_dict(a).to_dict()
        self.assertEqual(a, b)

    def test_for_coverage_completion(self):
        # Sorry, these tests are a bit silly ;)
        a = dict2()
        self.assertEqual(repr(a), 'dict2({})')

        a.__something__ = 100
        self.assertEqual(a.__something__, 100)
        self.assertNotIn('__something__', a)
        with self.assertRaises(AttributeError):
            print(a.__something_else__)
