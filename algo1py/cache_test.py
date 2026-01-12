from cache import *
import unittest

class test_cache(unittest.TestCase):
    def test_hashfun(self):
        nd = NativeCache(sz = 121)
        self.assertEqual(nd.hash_fun("cabcabc"), 99)
        self.assertEqual(nd.hash_fun("babcabb"), 98)
        self.assertEqual(nd.hash_fun("AbcabA"), 65)
        self.assertEqual(nd.hash_fun("A"), 65)
        self.assertEqual(nd.hash_fun(""), 0)
        self.assertEqual(nd.hash_fun("z"), 1)
        self.assertEqual(nd.hash_fun("}"), 4)    

    def test_seek(self):
        nd = NativeCache(sz = 5)
        self.assertEqual(nd.seek("A"), 0)
        self.assertEqual(nd.seek("B"), 1)
        nd.slots[0]="A"
        self.assertEqual(nd.seek("A1"), 1)
        nd.slots[1]="A1"
        self.assertEqual(nd.seek("B"), 2)
        nd.slots[4]="EE"
        self.assertEqual(nd.seek("E2"), 2)
        nd.slots[2]="C1"
        nd.slots[3]="C2"
        self.assertEqual(nd.seek("FUCK"), None)    

    def test_put(self):
        nd = NativeCache(sz = 5)
        nd.put("B", "valB")
        self.assertEqual(nd.slots, [None, "B", None, None, None])
        self.assertEqual(nd.values, [None, "valB", None, None, None])
        nd.put("B1", "valB1")
        self.assertEquals(nd.slots, [None, "B", "B1", None, None])
        self.assertEqual(nd.values, [None, "valB", "valB1", None, None])        
        nd.put("B2", "valB2")
        self.assertEquals(nd.slots, [None, "B", "B1", "B2", None])
        self.assertEqual(nd.values, [None, "valB", "valB1", "valB2", None])       
        nd.put("B3", "valB3")
        self.assertEquals(nd.slots, [None, "B", "B1", "B2", "B3"])
        self.assertEqual(nd.values, [None, "valB", "valB1", "valB2", "valB3"])          
        nd.put("C", "valC")
        self.assertEquals(nd.slots, ["C", "B", "B1", "B2", "B3"])
        self.assertEqual(nd.values, ["valC", "valB", "valB1", "valB2", "valB3"])                  
        self.assertEqual(nd.get("B"), "valB")
        self.assertEqual(nd.get("B"), "valB")
        nd.put("B4", "valB4")
        self.assertEqual(nd.values, ["valB4", "valB", "valB1", "valB2", "valB3"])                  
        self.assertEqual(nd.get("B4"), "valB4")
        self.assertEqual(nd.get("B4"), "valB4")
        nd.put("B5", "valB5")
        self.assertEqual(nd.values, ["valB4", "valB", "valB5", "valB2", "valB3"])                  
        self.assertEqual(nd.hits, [3, 3, 1, 1, 1])
        nd.put("B6", "valB6")
        self.assertEqual(nd.values, ["valB4", "valB", "valB6", "valB2", "valB3"])                  

if __name__ == "__main__":
    unittest.main()
