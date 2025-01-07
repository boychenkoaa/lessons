from unittest import TestCase, main
from snake_smart import * 

class test_comb(TestCase):
    def test_accumuate_distances(self):
        c = Comb([1, 2, 3, 1, 2, 3], pi/6, (0, 0))
        self.assertEqual(c.distances_acc, [1, 3, 6, 7, 9, 12])
    
    def test_from_distances_angle(self):
        c = Comb([1, 2, 3, 1, 2, 3], pi/6, (0, 0))
        self.assertAlmostEqual(distance_pp2(c.lines[0].v, (sqrt(3)/2, 1/2)), 0)
        self.assertAlmostEqual(distance_pp2(c.lines[5].v, (sqrt(3)/2, 1/2)), 0)
        self.assertEqual(c.distances_acc, [1, 3, 6, 7, 9, 12])
        self.assertAlmostEqual(distance_pp(c.lines[5].p, (-6, 6*sqrt(3))), 0)
    
    def test_find_point(self):
        c = Comb([1, 2, 3, 1, 2, 3], pi/6, (0, 0))
        self.assertEqual(c.bisect_point((0, 0)), 0)
        self.assertEqual(c.bisect_point((0, 3)), 1)
        
    def test_slice_segment(self):
        c = Comb([1, 2, 3, 1, 2, 3], pi/2, (0, 0))
        slice_result = c.slice_segment(Segment2(p=(0, 10), v=(-10, 0)))
        self.assertEqual(len(slice_result.pline), 5)
        slice_result = c.slice_segment(Segment2(p=(0, 10), v=(-13, 0)))
        self.assertEqual(len(slice_result.pline), 6)        
        slice_result = c.slice_segment(Segment2(p=(0, 10), v=(-1.2, 0)))
        self.assertEqual(len(slice_result.pline), 1)
        
class TestBeads(TestCase):
    def test_add_raster_point(self):
        beads = Beads(line = Line2(p = (0, 1), v = (1, 0)), raster_points = [], is_sorted = True)
        beads.add_raster_point(RasterPoint(point = (5, 5), segment_index = 0, contour_index = 0))        
        self.assertEqual(len(beads.raster_points), 1)
        self.assertEqual(beads.is_sorted, False)
        beads.add_raster_point(RasterPoint(point = (4, 4), segment_index = 0, contour_index = 0))
        self.assertEqual(len(beads.raster_points), 2)
        beads.add_raster_point(RasterPoint(point = (6, 6), segment_index = 0, contour_index = 0))
        self.assertEqual(len(beads.raster_points), 3)
        self.assertEqual(beads.is_sorted, False)
        self.assertEqual(beads.raster_points[0].point, (5, 1))
        self.assertEqual(beads.raster_points[1].point, (4, 1))
        self.assertEqual(beads.raster_points[2].point, (6, 1))
        
    def test_sort_points(self):
        beads = Beads(line = Line2(p = (0, 1), v = (-1, 0)), raster_points = [], is_sorted = True)
        beads.add_raster_point(RasterPoint(point = (5, 5), segment_index = 0, contour_index = 0))        
        beads.add_raster_point(RasterPoint(point = (4, 4), segment_index = 0, contour_index = 0))
        beads.add_raster_point(RasterPoint(point = (6, 6), segment_index = 0, contour_index = 0))
        beads.add_raster_point(RasterPoint(point = (3, 3), segment_index = 0, contour_index = 0))
        beads.sort_points()
        self.assertEqual(beads.raster_points[0].point, (6, 1))
        self.assertEqual(beads.raster_points[-1].point, (3, 1))
    
class testRaster(TestCase):
    def test_from_beads(self):
        beads = Beads(line = Line2(p = (0, 1), v = (-1, 0)), raster_points = [], is_sorted = True)
        beads.add_raster_point(RasterPoint(point = (5, 5), segment_index = 0, contour_index = 0))        
        beads.add_raster_point(RasterPoint(point = (4, 4), segment_index = 0, contour_index = 0))
        beads.add_raster_point(RasterPoint(point = (6, 6), segment_index = 0, contour_index = 0))
        beads.add_raster_point(RasterPoint(point = (3, 3), segment_index = 0, contour_index = 0))        
        raster = Raster()
        raster.from_beads(beads)
        self.assertEqual(len(raster.segments), 2)
        self.assertEqual(raster.segments[0][B].point, (6, 1))
        self.assertEqual(raster.segments[0][E].point, (5, 1))
        self.assertEqual(raster.segments[1][B].point, (4, 1))
        self.assertEqual(raster.segments[1][E].point, (3, 1))
        self.assertTrue(raster.is_dash_line)
    
    def test_add_segment(self):
        beads = Beads(line = Line2(p = (0, 1), v = (-1, 0)), raster_points = [], is_sorted = True)
        beads.add_raster_point(RasterPoint(point = (5, 5), segment_index = 0, contour_index = 0))        
        beads.add_raster_point(RasterPoint(point = (4, 4), segment_index = 0, contour_index = 0))
        beads.add_raster_point(RasterPoint(point = (6, 6), segment_index = 0, contour_index = 0))
        beads.add_raster_point(RasterPoint(point = (3, 3), segment_index = 0, contour_index = 0))        
        raster = Raster()
        raster.from_beads(beads)
        
        
if __name__ == "__main__":
    main()
    