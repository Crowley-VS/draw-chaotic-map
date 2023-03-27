from unittest import TestCase
from chaotic_maps import TinkerbellMap, ChaoticMap, IkedaMap
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