import unittest
from geom_raw import * 
from editor2d import *
from math import pi, sin, cos

class testSegment2(unittest.TestCase):
    def test_BE(self):
        x1, y1, x2, y2 = (1, 2), (3, 4)
        s = Segment2(x1, y2, x2, y2)        
        self.assertEqual(s.begin, (x1, y1))
        self.assertEqual(s.begin, (x2, y2))
        
    def test_reversed(self):
        x1, y1, x2, y2 = (1, 2), (3, 4)
        s = Segment2(x1, y2, x2, y2)
        s_rev = s.reversed
        self.assertEqual(s_rev.begin, s.end)
        self.assertEqual(s_rev.end, s.begin)
        
    def test_length_simple(self):
        s = Segment2((1, 2), (3, 4))
        self.assertAlmostEqual(s.length, 2**1.5)
        s = Segment2((1, 2), (1, 2))
        self.assertAlmostEqual(s.length, 0)

class testArc2(unittest.TestCase):
    def test_BE(self):
        x1, y1, x2, y2, x3, y3 = 1, 2, 3, 4, 5, 6
        a = Arc2((x1, y1), (x2, y2), (x3, y3))
        self.assertEqual((a.begin, a.end), ((x1, y1), (x3, y3)))
    
    def test_is_valid(self):
        x1, y1, x3, y3 = 1, 2, 3, 4
        x2, y2 = (x1 + x3) / 2.0,  (y1 + y3) / 2.0
        a = Arc2((x1, y1), (x2, y2), (x3, y3))
        self.assertEqual(a.last_status, CommandStatus.FAIL)
        b = Arc2((x1+1, y1), (x2, y2), (x3, y3))
        self.assertEqual(b.last_status, CommandStatus.OK)
                             
    def test_from_center_radius_angles(self):
        xc, yc = 1, 2
        R = 1.5
        angle1 = 0
        angle2 = pi / 2
        center = xc, yc
        angle = abs(angle1 - angle2)
        a = Arc2((0, 0), (0, 0), (0, 0))
        a.from_center_radius_angles(center, R, angle1, angle2)
        self.assertEqual(a.last_status, CommandStatus.OK)
        self.assertAlmostEqual(angle(a.begin, a.center, a.end), angle)
        self.assertAlmostEqual(angle, a.angle)
        self.assertAlmostEqual(distance_pp(a.begin, a.end), 2 * R * sin(angle/2.0))
        
    def test_angle_center(self):
        x1, y1, x3, y3 = 1, 2, 3, 4
        x2, y2 = (x1 + x3) / 2.0, (y1 + y3) / 2.0
        x1 += 1
        a = Arc2((x1, y1), (x2, y2), (x3, y3))
        self.assertEqual(a.last_status, CommandStatus.OK)
        self.assertAlmostEqual(distance_pp(a.center, a.begin), a.radius)
        self.assertAlmostEqual(distance_pp(a.center, a.mid), a.radius)
        self.assertAlmostEqual(distance_pp(a.center, a.end), a.radius)
        self.assertGreaterEqual(a.angle, -2*pi)
        self.assertLessEqual(a.angle, 2*pi)
    
    def test_reversed(self):
        x1, y1, x3, y3 = 1, 2, 3, 4
        x2, y2 = (x1 + x3) / 2.0, (y1 + y3) / 2.0
        x1 += 1
        a = Arc2((x1, y1), (x2, y2), (x3, y3))        
        b = a.reversed
        self.assertEqual(a.begin, b.end)
        self.assertEqual(a.end, b.begin)
        self.assertAlmostEqual(a.angle, -b.angle)
        self.assertAlmostEqual(a.radius, b.radius)
        
    def test_raw(self):
        x1, y1, x2, y2, x3, y3 = 1, 2, 3, 4, 5, 6
        a = Arc2((x1, y1), (x2, y2), (x3, y3))
        self.assertEqual(a.raw, (a.begin, a.mid, a.end))
        
class testPline2(unittest.TestCase):
    def test_init(self):
        point_list = [(0, 0)]
        pline = Pline2(point_list)
        self.assertEqual(pline.last_status, CommandStatus.FAIL)
        point_list = [(0, 0), (1, 1)]
        pline = Pline2(point_list)
        self.assertEqual(pline.last_status, CommandStatus.OK)        
    
    def test_be(self):
        x1, y1, x2, y2 = 1, 2, 3, 4
        N = 10
        pline = Pline2([(x1, y2)] + [(0, 0)] * N + [(x2, y2)])
        if pline.last_status == CommandStatus.OK:
            self.assertEqual(pline.begin, (x1, y1))
            self.assertEqual(pline.end, (x2, y2))
    
    def test_length_reversed(self):
        point_list = [(1, 2), (3, 4), (5, 6), (7, 8)]
        pline = Pline2(point_list)
        pline_rev = pline.reversed 
        if pline_rev.last_status == CommandStatus.OK:
            self.assertAlmostEqual(pline_rev.length, pline.length)
            self.assertAlmostEqual(pline_rev.begin, pline.end)
            self.assertAlmostEqual(pline_rev.end, pline.begin)
            self.assertEqual(pline_rev.points_number, pline.points_number)
    
    def test_add(self):
        pline = Pline2([(1, 2), (3, 4), (5, 6), (7, 8)])
        self.assertEqual(pline.points_number, 4)
        pline.add(-1, (0, 0))
        pline.add(0, (11, 12))
        self.assertEqual(pline[-1], (0, 0))
        self.assertEqual(pline[0], (11, 12))
        pline.add(2, (14, 14))
        self.assertEqual(pline[2], (14, 14))
        self.assertEqual(pline.points_number, 7)
        
    
    def test_getitem(self):
        pline = Pline2([(1, 2), (3, 4), (5, 6), (7, 8)])
        self.assertEqual(pline[0], (1, 2))
        self.assertEqual(pline[1], (3, 4))
        self.assertEqual(pline[2], (5, 6))
        self.assertEqual(pline[3], (7, 8))
        self.assertEqual(pline[-4], (1, 2))
        self.assertEqual(pline[-3], (3, 4))
        self.assertEqual(pline[-2], (5, 6))
        self.assertEqual(pline[-1], (7, 8))
        
    def test_move(self):
        pline = Pline2([(1, 2), (3, 4), (5, 6), (7, 8)])
        pline.moveB(11, 12)
        self.assertEqual(pline.begin, (11, 12))
        pline.move(0, (1, 2))
        self.assertEqual(pline.begin, (1, 2))
        pline.move(-1, (17, 18))
        self.assertEqual(pline.end, (17, 18))
        pline.moveE((7, 8))
        self.assertEqual(pline.end, (7, 8))
        pline.move(1, (13, 14))
        self.assertEqual(pline[1], (13, 14))
        
    def test_points_number(self):
        pline = Pline2([(1, 2), (3, 4), (5, 6), (7, 8)])
        self.assertEqual(pline.points_number, 4)
        
        

class testPline2(unittest.TestCase):
    ...

if __name__ == "__main__":
    unittest.main()
