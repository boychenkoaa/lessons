from bloom import *
import unittest

def cycle_shift(str1):
    if str1:
        return str1[1:] + str1[0]
    return str1
    

class test_bloom(unittest.TestCase):
    def test_all(self):
        strlist = ["0123456789"]
        for i in range(9):
            strlist.append(cycle_shift(strlist[-1]))        
        bf = BloomFilter(32)
        for s in strlist:
            bf.add(s)
        for s in strlist:
            self.assertEqual(bf.is_value(s), True)
            self.assertEqual(bf.is_value(s+"a"), False)


if __name__ == '__main__':
    unittest.main()
    