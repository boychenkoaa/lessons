from dict1 import *
import unittest

class test_dict1(unittest.TestCase):
    def test_hashfun(self):
        nd = NativeDictionary(sz = 121)
        self.assertEqual(nd.hash_fun("cabcabc"), 99)
        self.assertEqual(nd.hash_fun("babcabb"), 98)
        self.assertEqual(nd.hash_fun("AbcabA"), 65)
        self.assertEqual(nd.hash_fun("A"), 65)
        self.assertEqual(nd.hash_fun(""), 0)
        self.assertEqual(nd.hash_fun("z"), 1)
        self.assertEqual(nd.hash_fun("}"), 4)        
        
    def test_seek(self):
        nd = NativeDictionary(sz = 5)
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
        nd = NativeDictionary(sz = 5)
        nd.put("B", "val_B")
        self.assertEqual(nd.slots, [None, "B", None, None, None])
        self.assertEqual(nd.values, [None, "val_B", None, None, None])
        nd.put("B1", "val_B1")
        self.assertEquals(nd.slots, [None, "B", "B1", None, None])
        self.assertEqual(nd.values, [None, "val_B", "val_B1", None, None])        
        nd.put("B", "new_val_B")
        self.assertEquals(nd.slots, [None, "B", "B1", None, None])
        self.assertEqual(nd.values, [None, "new_val_B", "val_B1", None, None])     
        
    def test_iskey(self):
        nd = NativeDictionary(sz = 5)
        nd.put("B", "val_B")        
        nd.put("B1", "val_B1")
        nd.put("C", "val_C")
        self.assertTrue(nd.is_key("B1"))
        self.assertTrue(nd.is_key("B"))
        self.assertTrue(nd.is_key("C"))
        self.assertFalse(nd.is_key("D"))
        
    def test_get(self):
        nd = NativeDictionary(sz = 5)
        nd.put("B", "val_B")        
        nd.put("B1", "val_B1")
        nd.put("C", "val_C")
        self.assertEqual(nd.get("B"), "val_B")
        self.assertEqual(nd.get("B1"), "val_B1")
        self.assertEqual(nd.get("C"), "val_C")
        self.assertEqual(nd.get("D"), None)
        
    
    
if __name__ == '__main__':
    unittest.main()

    
