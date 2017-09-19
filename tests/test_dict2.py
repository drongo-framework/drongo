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

    def test_property(self):
        a = dict2.from_dict({'a': {'b': 10}})
        b = a.get_property('a.b')
        self.assertEqual(b, 10)
        self.assertIsNone(a.get_property('a.c'))

    def test_update(self):
        a = dict2.from_dict({'a': {'b': 10}, 'b': 10})
        b = dict2.from_dict({'a': {'b': 20}})

        a.update(b)
        self.assertEqual(a, {'a': {'b': 20}, 'b': 10})

        a = dict2.from_dict({})
        b = dict2.from_dict({'a': {'b': 20}})

        a.update(b)
        self.assertEqual(a, {'a': {'b': 20}})

    def test_set_get(self):
        a = dict2()
        a.a = 10
        a.b.c = 20
        a.x = {'y': 30}

        self.assertEqual(a.a, 10)
        self.assertEqual(a.b.c, 20)
        self.assertEqual(a.x.y, 30)
