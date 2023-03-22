from unittest import TestCase
from chaotic_maps import TinkerbellMapSystem

class TestTinkerbellMapSystem(TestCase):
    def setUp(self):
        self.tinkerbellmapsys1 = TinkerbellMapSystem(0.9, -0.6013, 2, 0.5, 10, 1, -0.72, -0.64)
        self.tinkerbellmapsys2 = TinkerbellMapSystem(0.9, -0.6013, 2, 0.5, 10, 1)
    def test_calculate_points(self):
        self.tinkerbellmapsys1.calculate_points()
        xs1, ys1 = self.tinkerbellmapsys1.get_points()
        self.assertEqual(xs1[1], (-0.72)**2 - (-0.64)**2 + 0.9*-0.72 + -0.6013*-0.64)
        self.assertEqual(ys1[1], 2*(-0.72)*(-0.64) + 2*(-0.72) + 0.5*(-0.64))
        self.tinkerbellmapsys2.calculate_points()
        xs2, ys2 = self.tinkerbellmapsys2.get_points()
        self.assertEqual(xs2[1], 0.1**2 - 0.1**2 + 0.9*0.1 + -0.6013*0.1)
        self.assertEqual(ys2[1], 2*0.1*0.1 + 2*0.1 + 0.5*0.1)