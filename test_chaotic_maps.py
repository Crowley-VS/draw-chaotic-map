from unittest import TestCase
from chaotic_maps import TinkerbellMap, ChaoticMap, IkedaMap, BogdanovMap, GingerbreadMap, StandardMap, CliffordAttractor, GumowskiMiraAttractor
from math import sin, cos

class TestChaoticMap(TestCase):
    def setUp(self) -> None:
        self.chaotic_map = ChaoticMap(0, 0)
    def test_reset_origin(self):
        self.chaotic_map.reset_origin(1, 1)
        self.assertEqual(self.chaotic_map.xs[0], 1)
        self.assertEqual(self.chaotic_map.ys[0], 1)

class TestTinkerbellMap(TestCase):
    def setUp(self):
        self.tinkerbellmap1 = TinkerbellMap(0.9, -0.6013, 2, 0.5, -0.72, -0.64)
        self.tinkerbellmap2 = TinkerbellMap(0.9, -0.6013, 2, 0.5)
    def test_calculate(self):
        x, y = self.tinkerbellmap1.step(-0.72, -0.64)
        self.assertEqual(x, (-0.72)**2 - (-0.64)**2 + 0.9*-0.72 + -0.6013*-0.64)
        self.assertEqual(y, 2*(-0.72)*(-0.64) + 2*(-0.72) + 0.5*(-0.64))
    def test_calculate_points(self):
        self.tinkerbellmap1.calculate(0)
        xs1, ys1 = self.tinkerbellmap1.get_points()
        self.assertEqual(xs1[1], (-0.72)**2 - (-0.64)**2 + 0.9*-0.72 + -0.6013*-0.64)
        self.assertEqual(ys1[1], 2*(-0.72)*(-0.64) + 2*(-0.72) + 0.5*(-0.64))

        self.tinkerbellmap2.calculate(0)
        xs2, ys2 = self.tinkerbellmap2.get_points()
        self.assertEqual(xs2[1], 0.1**2 - 0.1**2 + 0.9*0.1 + -0.6013*0.1)
        self.assertEqual(ys2[1], 2*0.1*0.1 + 2*0.1 + 0.5*0.1)

class TestIkedaMap(TestCase):
    def setUp(self):
        self.ikedamap1 = IkedaMap(0.918, 1, 1)
        self.ikedamap2 = IkedaMap(0.7, 2, 2)

    def test_calculate(self):
        x, y = self.ikedamap1.step(1, 1)
        t = 0.4 - 6/(1 + 1**2 + 1**2)
        self.assertEqual(x, 1 + 0.918 * (1*cos(t) - 1*sin(t)))
        self.assertEqual(y, 0.918 * (1*sin(t) + 1*cos(t)))
    def test_calculate_points(self):
        self.ikedamap1.calculate(0)
        xs1, ys1 = self.ikedamap1.get_points()
        t = 0.4 - 6/(1 + 1**2 + 1**2)
        self.assertEqual(xs1[1], 1 + 0.918 * (1*cos(t) - 1*sin(t)))
        self.assertEqual(ys1[1], 0.918 * (1*sin(t) + 1*cos(t)))

        self.ikedamap2.calculate(0)
        xs2, ys2 = self.ikedamap2.get_points()
        t = 0.4 - 6/(1 + 2**2 + 2**2)
        self.assertEqual(xs2[1], 1 + 0.7 * (2*cos(t) - 2*sin(t)))
        self.assertEqual(ys2[1], 0.7 * (2*sin(t) + 2*cos(t)))

class TestBogdanovMap(TestCase):
    def setUp(self):
        self.bogdanovmap = BogdanovMap(0, 1.2, 0, 0.05, 0.05)

    def test_calculate(self):
        x0 = y0 = 0.05
        x, y = self.bogdanovmap.step(x0, y0)
        y_test = y0*(1+0+0*x0) + 1.2*x0*(x0-1)
        x_test = x0+y_test
        self.assertEqual(x, x_test)
        self.assertEqual(y, y_test)
    def test_calculate_points(self):
        self.bogdanovmap.calculate(0)
        xs1, ys1 = self.bogdanovmap.get_points()
        x0 = y0 = 0.05
        y_test = y0*(1+0+0*x0) + 1.2*x0*(x0-1)
        x_test = x0+y_test
        self.assertEqual(xs1[1], x_test)
        self.assertEqual(ys1[1], y_test)

class TestGingerbreadMap(TestCase):
    def setUp(self):
        self.gingerbreadmap = GingerbreadMap(0.5, 0.5)

    def test_calculate(self):
        x0 = y0 = 0.5
        x, y = self.gingerbreadmap.step(x0, y0)
        x_test = 1 - y0 + abs(x0)
        y_test = x0
        self.assertEqual(x, x_test)
        self.assertEqual(y, y_test)
    def test_calculate_points(self):
        self.gingerbreadmap.calculate(0)
        xs1, ys1 = self.gingerbreadmap.get_points()
        x0 = y0 = 0.5
        x_test = 1 - y0 + abs(x0)
        y_test = x0
        self.assertEqual(xs1[1], x_test)
        self.assertEqual(ys1[1], y_test)

class TestStandardMap(TestCase):
    def setUp(self):
        self.gingerbreadmap = StandardMap(1.5,1,1)

    def test_calculate(self):
        x0 = y0 = 1
        x, y = self.gingerbreadmap.step(x0, y0)
        y_test = y0 + 1.5 * sin(x0)
        x_test = x0 + y_test
        self.assertEqual(x, x_test)
        self.assertEqual(y, y_test)
    def test_calculate_points(self):
        self.gingerbreadmap.calculate(0)
        xs1, ys1 = self.gingerbreadmap.get_points()
        x0 = y0 = 1
        y_test = y0 + 1.5 * sin(x0)
        x_test = x0 + y_test
        self.assertEqual(xs1[1], x_test)
        self.assertEqual(ys1[1], y_test)

class TestCliffordAttractor(TestCase):
    def setUp(self):
        self.cmap = CliffordAttractor()

    def test_step(self):
        x, y = self.cmap.step(0.1, 0.1)
        expected_x = sin(self.cmap.a * 0.1) + self.cmap.c * cos(self.cmap.a * 0.1)
        expected_y = sin(self.cmap.b * 0.1) + self.cmap.d * cos(self.cmap.b * 0.1)
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(y, expected_y)


class TestGumowskiMiraAttractor(TestCase):
    def setUp(self):
        self.gmap = GumowskiMiraAttractor()

    def test_step(self):
        x, y = self.gmap.step(0.1, 0.1)
        expected_x = self.gmap.b * 0.1 + self.gmap.supporting_func(0.1)
        expected_y = self.gmap.supporting_func(expected_x) - 0.1
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(y, expected_y)

    def test_supporting_func(self):
        x = 0.1
        expected = self.gmap.a * x + 2 * (1 - self.gmap.a) * x ** 2 * (1 + x ** 2) ** (-2)
        self.assertAlmostEqual(self.gmap.supporting_func(x), expected)
class TestChaoticMapGetAttribute(TestCase):

    def setUp(self):
        # Create a ChaoticMap instance with sample values
        self.map = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=True,
            default_range=(0, 10, -5, 5, 0.1),
            sim_range=[]
        )

    def test_get_attribute_existing(self):
        self.assertEqual(self.map.get_attribute('a'), 0.5)
        self.assertEqual(self.map.get_attribute('b'), 0.2)
        self.assertEqual(self.map.get_attribute('c'), 0.8)
        self.assertEqual(self.map.get_attribute('d'), 0.4)
        self.assertEqual(self.map.get_attribute('x0'), 1.0)
        self.assertEqual(self.map.get_attribute('y0'), 2.0)
        self.assertEqual(self.map.get_attribute('xmin'), 0)
        self.assertEqual(self.map.get_attribute('xmax'), 10)
        self.assertEqual(self.map.get_attribute('ymin'), -5)
        self.assertEqual(self.map.get_attribute('ymax'), 5)
        self.assertEqual(self.map.get_attribute('step_size'), 0.1)

    def test_get_attribute_nonexistent(self):
        self.assertIsNone(self.map.get_attribute('invalid_attr'))
        self.assertIsNone(self.map.get_attribute('k'))

    def test_get_attribute_not_multi_point_sim(self):
        map_single = ChaoticMap(x0=1.0, y0=2.0)
        self.assertIsNone(map_single.get_attribute('xmin'))
        self.assertIsNone(map_single.get_attribute('xmax'))
        self.assertIsNone(map_single.get_attribute('ymin'))
        self.assertIsNone(map_single.get_attribute('ymax'))
        self.assertIsNone(map_single.get_attribute('step_size'))

    def test_get_attribute_no_sim_range(self):
        map_no_range = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=True,
            default_range=(0, 10, -5, 5, 0.1),
            sim_range=[]
        )
        self.assertEqual(map_no_range.get_attribute('xmin'), 0)
        self.assertEqual(map_no_range.get_attribute('xmax'), 10)
        self.assertEqual(map_no_range.get_attribute('ymin'), -5)
        self.assertEqual(map_no_range.get_attribute('ymax'), 5)
        self.assertEqual(map_no_range.get_attribute('step_size'), 0.1)
class TestChaoticMapSetAttribute(TestCase):

    def setUp(self):
        # Create a ChaoticMap instance with sample values
        self.map = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=True,
            default_range=(0, 10, -5, 5, 0.1),
            sim_range=[]
        )

    def test_set_attribute_existing(self):
        self.map.set_attribute('a', 0.3)
        self.assertEqual(self.map.get_attribute('a'), 0.3)
        self.map.set_attribute('b', 0.1)
        self.assertEqual(self.map.get_attribute('b'), 0.1)
        self.map.set_attribute('x0', 2.5)
        self.assertEqual(self.map.get_attribute('x0'), 2.5)

    def test_set_attribute_range(self):
        self.map.set_attribute('xmin', -5)
        self.assertEqual(self.map.get_attribute('xmin'), -5)
        self.map.set_attribute('xmax', 15)
        self.assertEqual(self.map.get_attribute('xmax'), 15)
        self.map.set_attribute('ymin', -10)
        self.assertEqual(self.map.get_attribute('ymin'), -10)
        self.map.set_attribute('ymax', 10)
        self.assertEqual(self.map.get_attribute('ymax'), 10)
        self.map.set_attribute('step_size', 0.2)
        self.assertEqual(self.map.get_attribute('step_size'), 0.2)

    def test_set_attribute_nonexistent(self):
        self.map.set_attribute('invalid_attr', 123)
        self.assertIsNone(self.map.get_attribute('invalid_attr'))
        self.map.set_attribute('z', 456)
        self.assertIsNone(self.map.get_attribute('z'))

    def test_set_attribute_no_sim_range(self):
        map_no_range = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=True,
            default_range=(0, 10, -5, 5, 0.1),
            sim_range=[]
        )
        map_no_range.set_attribute('xmin', -5)
        self.assertEqual(map_no_range.get_attribute('xmin'), -5)
        map_no_range.set_attribute('xmax', 15)
        self.assertEqual(map_no_range.get_attribute('xmax'), 15)
        map_no_range.set_attribute('ymin', -10)
        self.assertEqual(map_no_range.get_attribute('ymin'), -10)
        map_no_range.set_attribute('ymax', 10)
        self.assertEqual(map_no_range.get_attribute('ymax'), 10)
        map_no_range.set_attribute('step_size', 0.2)
        self.assertEqual(map_no_range.get_attribute('step_size'), 0.2)

    def test_set_attribute_without_sim_range_range_attributes(self):
        map_no_range = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=False,
            default_range=(),
            sim_range=[]
        )
        with self.assertRaises(ValueError):
            map_no_range.set_attribute('xmin', -2)
        with self.assertRaises(ValueError):
            map_no_range.set_attribute('xmax', 8)
        with self.assertRaises(ValueError):
            map_no_range.set_attribute('ymin', -3)
        with self.assertRaises(ValueError):
            map_no_range.set_attribute('ymax', 4)
        with self.assertRaises(ValueError):
            map_no_range.set_attribute('step_size', 0.2)
    def test_set_attribute_with_sim_range(self):
        map_with_range = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=True,
            default_range=(0, 10, -5, 5, 0.1),
            sim_range=[-2, 2, -1, 1, 0.2]
        )
        map_with_range.set_attribute('xmin', -5)
        self.assertEqual(map_with_range.get_attribute('xmin'), -5)
        map_with_range.set_attribute('xmax', 15)
        self.assertEqual(map_with_range.get_attribute('xmax'), 15)
        map_with_range.set_attribute('ymin', -10)
        self.assertEqual(map_with_range.get_attribute('ymin'), -10)
        map_with_range.set_attribute('ymax', 10)
        self.assertEqual(map_with_range.get_attribute('ymax'), 10)
        map_with_range.set_attribute('step_size', 0.2)
        self.assertEqual(map_with_range.get_attribute('step_size'), 0.2)

    def test_set_attribute_without_sim_range(self):
        map_no_range = ChaoticMap(
            x0=1.0,
            y0=2.0,
            a=0.5,
            b=0.2,
            c=0.8,
            d=0.4,
            is_multi_point_sim=False,
            default_range=(),
            sim_range=[]
        )
        map_no_range.set_attribute('a', 0.3)
        self.assertEqual(map_no_range.get_attribute('a'), 0.3)
        map_no_range.set_attribute('b', 0.1)
        self.assertEqual(map_no_range.get_attribute('b'), 0.1)
        map_no_range.set_attribute('x0', 2.5)
        self.assertEqual(map_no_range.get_attribute('x0'), 2.5)
