from hashtable import *
import unittest

class test_hash(unittest.TestCase):
    
    def test_hashfun(self):
        h = HashTable(sz = 121, stp = 1)
        self.assertEqual(h.hash_fun("cabcabc"), 99)
        self.assertEqual(h.hash_fun("babcabb"), 98)
        self.assertEqual(h.hash_fun("AbcabA"), 65)
        self.assertEqual(h.hash_fun("A"), 65)
        self.assertEqual(h.hash_fun(""), 0)
        self.assertEqual(h.hash_fun("z"), 1)
        self.assertEqual(h.hash_fun("}"), 4)
        
    def test_seekslot(self):
        h = HashTable(sz = 5, stp = 1)
        h.slots[2] = "a"
        h.slots[3] = "aa"
        h.slots[4] = "aaa"
        self.assertEqual(h.seek_slot("aaaa"), 0)
        h.slots[0] = ""
        self.assertEqual(h.seek_slot("aaaa"), 1)
        h.slots[1] = ""
        self.assertEqual(h.seek_slot("aaaa"), None)
        
    def test_put(self):
        h = HashTable(sz = 5, stp = 2)
        h.put("")
        self.assertEqual(h.slots, ["", None, None, None, None])        
        h.put("a")
        self.assertEqual(h.slots, ["", None, "a", None, None])
        h.put("aa")
        self.assertEqual(h.slots, ["", None, "a", None, "aa"])
        h.put("aaa")
        self.assertEqual(h.slots, ["", "aaa", "a", None, "aa"])
        h.put("aaaa")
        self.assertEqual(h.slots, ["", "aaa", "a", "aaaa", "aa"])
    
    def test_find(self):
        h = HashTable(sz = 5, stp = 1)
        h.put("a")
        h.put("aa")
        h.put("aaa")
        h.put("aaaa")
        self.assertEqual(h.find("aaaa"), 0)
        self.assertEqual(h.find("aaa"), 4)
        self.assertEqual(h.find("aa"), 3)
        self.assertEqual(h.find("a"), 2)
        self.assertEqual(h.find("b"), None)

if __name__ == '__main__':
    unittest.main()
