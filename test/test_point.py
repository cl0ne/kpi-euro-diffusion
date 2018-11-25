import unittest
from euro_diffusion.point import Point


class PointCase(unittest.TestCase):
    a = Point(1, 1)
    b = Point(1, 1)
    c = Point(-1, -1)
    d = Point(-1, -1)
    e = Point(2, 1)

    x = Point(1, 0)
    y = Point(0, 1)
    z = Point(0, 0)

    def test_equal(self):
        self.assertEqual(self.a, self.a)
        self.assertEqual(self.c, self.c)
        self.assertEqual(self.a, self.b)
        self.assertEqual(self.c, self.d)
        self.assertNotEqual(self.a, self.c)
        self.assertNotEqual(self.c, self.a)
        self.assertNotEqual(self.a, self.e)
        self.assertNotEqual(self.a, self.x)
        self.assertNotEqual(self.a, self.y)
        self.assertNotEqual(self.a, self.z)

    def test_less(self):
        self.assertLess(self.z, self.a)
        self.assertLess(self.c, self.z)

        self.assertLess(self.x, self.a)
        self.assertLess(self.y, self.a)
        self.assertLess(self.z, self.y)
        self.assertLess(self.z, self.x)

        self.assertLess(self.c, self.a)
        self.assertLess(self.a, self.e)

    def test_less_equal(self):
        self.assertLessEqual(self.a, self.a)
        self.assertLessEqual(self.c, self.c)
        self.assertLessEqual(self.z, self.z)
        self.assertLessEqual(self.x, self.x)
        self.assertLessEqual(self.y, self.y)

        self.assertLessEqual(self.z, self.a)
        self.assertLessEqual(self.c, self.z)

        self.assertLessEqual(self.x, self.a)
        self.assertLessEqual(self.y, self.a)
        self.assertLessEqual(self.z, self.y)
        self.assertLessEqual(self.z, self.x)

        self.assertLessEqual(self.c, self.a)
        self.assertLessEqual(self.a, self.e)

    def test_add(self):
        self.assertEqual(self.z, self.a + self.c)
        self.assertEqual(self.a, self.x + self.y)
        self.assertEqual(self.e, self.a + self.x)
        self.assertEqual(self.a, self.a + self.z)
        self.assertEqual(self.c, self.c + self.z)
        self.assertEqual(self.e, self.e + self.z)
        self.assertEqual(self.z, self.z + self.z)

    def test_sub(self):
        self.assertLessEqual(self.z, self.a - self.a)
        self.assertEqual(self.a, self.a - self.z)
        self.assertEqual(self.c, self.c - self.z)
        self.assertEqual(self.e, self.e - self.z)
        self.assertEqual(self.c, self.z - self.a)
        self.assertLessEqual(self.z, self.z - self.z)


if __name__ == '__main__':
    unittest.main()
