from powerset import *
import unittest

import random

def randomstr(length: int):
    ans = ""
    for i in range(length):
        ans += chr(random.randint(97, 125))
    return ans
    

class test_powerset(unittest.TestCase):
    def test_put(self):
        ps1 = PowerSet()
        ps1.put("abc")
        self.assertEqual(ps1.size(), 1)
        ps1.put("fgh")
        self.assertEqual(ps1.size(), 2)        
        ps1.put("abc")
        self.assertEqual(ps1.size(), 2)
        ps1.put("ttt")
        self.assertEqual(ps1.size(), 3)
        
    def test_remove(self):
        ps1 = PowerSet()
        ps1.put("abc")        
        ps1.put("fgh")
        ps1.put("ttt")
        self.assertEqual(ps1.size(), 3)
        self.assertEqual(ps1.remove("ttt"), True)
        self.assertEqual(ps1.size(), 2)
        self.assertEqual(ps1.remove("ttt"), False)
        self.assertEqual(ps1.size(), 2)
        
    def test_union(self):
        ps1 = PowerSet()
        ps1.put("abc")        
        ps1.put("fgh")
        ps1.put("ttt")
        ps2 = PowerSet()
        ps3 = PowerSet()
        ps3.put("abc")        
        ps3.put("fgh2")
        ps3.put("ttt")                
        u12 = ps1.union(ps2)
        u13 = ps1.union(ps3)
        u23 = ps2.union(ps3)
        self.assertEqual(u12.size(), 3)
        self.assertEqual(u13.size(), 4)
        self.assertEqual(u23.size(), 3)
        
    def test_diff(self):
        ps1 = PowerSet()
        ps1.put("abc")        
        ps1.put("fgh")
        ps1.put("ttt")
        ps2 = PowerSet()
        ps3 = PowerSet()
        ps3.put("abc")        
        ps3.put("fgh2")
        ps3.put("ttt")                
        d12 = ps1.difference(ps2)
        d13 = ps1.difference(ps3)
        d23 = ps2.difference(ps3)
        self.assertEqual(d12.size(), 3)
        self.assertEqual(d13.size(), 1)
        self.assertEqual(d23.size(), 0)
    
    def test_sub(self):
        ps1 = PowerSet()
        ps1.put("abc")        
        ps1.put("fgh")
        ps1.put("ttt")
        ps2 = PowerSet()
        ps3 = PowerSet()
        ps3.put("abc")        
        ps3.put("ttt")                
        self.assertEqual(ps1.issubset(ps2), True)
        self.assertEqual(ps1.issubset(ps3), True)
        self.assertEqual(ps2.issubset(ps3), False)    
        self.assertEqual(ps3.issubset(ps1), False)
    
    def test_bigsize(self):
        ps1 = PowerSet()
        N = 20000
        for i in range(N):
            ps1.put(randomstr(5))
        
        ps2 = PowerSet()
        ps1.put("abc")        
        ps1.put("fgh")
        ps1.put("ttt")        
        
        u12 = ps1.union(ps2)
        self.assertEqual(u12.issubset(ps1), True)
        self.assertEqual(u12.issubset(ps2), True)
        self.assertEqual(u12.size(), ps1.size()+ps2.size())        
        
        du1 = u12.difference(ps1)
        self.assertEqual(du1.size(), ps2.size())        
                
        i12 = ps1.intersection(ps2)
        self.assertEqual(i12.size(), 0)
        
        iu1 = u12.intersection(ps1)
        self.assertEqual(iu1.size(), ps1.size())
        
        
        

if __name__ == '__main__':
    unittest.main()

