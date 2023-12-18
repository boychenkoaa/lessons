import unittest
from ordered_list import * 

class Test_OL(unittest.TestCase):
    def test_compare(self):
        ol = OrderedList(True)
        self.assertEqual(ol.compare(4, 5), -1)
        self.assertEqual(ol.compare(5, 5), 0)
        self.assertEqual(ol.compare(6, 5), 1)

    def test_add(self):
        ol = OrderedList(True)
        ol.add(6)
        self.assertEqual(ol.values(), [6])
        ol.add(5)
        self.assertEqual(ol.values(), [5, 6])
        ol.add(4)
        self.assertEqual(ol.values(), [4, 5, 6])
        ol.add(7)
        self.assertEqual(ol.values(), [4, 5, 6, 7])
        
    def test_find(self):
        ol = OrderedList(True)
        ol.add(6)
        ol.add(5)
        ol.add(4)
        ol.add(7)
        self.assertEqual(ol.find(4).value, 4)
        self.assertEqual(ol.find(5).value, 5)
        self.assertEqual(ol.find(6).value, 6)
        self.assertEqual(ol.find(7).value, 7)
        self.assertEqual(ol.find(-1), None)
        
    def test_del(self):
        ol = OrderedList(True)
        ol.add(6)
        ol.add(5)
        ol.add(4)
        ol.add(7)
        self.assertEqual(ol.values(), [4, 5, 6, 7])
        ol.delete(5)
        self.assertEqual(ol.values(), [4, 6, 7])
        ol.delete(7)
        self.assertEqual(ol.values(), [4, 6])
        ol.delete(6)
        self.assertEqual(ol.values(), [4])
        ol.delete(4)
        self.assertEqual(ol.values(), [])
        

class Test_OSL(unittest.TestCase):
    def test_compare(self):
        ol = OrderedStringList(True)
        self.assertEqual(ol.compare("4", "5"), -1)
        self.assertEqual(ol.compare("5", "5"), 0)
        self.assertEqual(ol.compare("6", "5"), 1)
        self.assertEqual(ol.compare("  4  ", " 5   "), -1)
        self.assertEqual(ol.compare("5", "5    "), 0)
        self.assertEqual(ol.compare("6   ", " 5"), 1)        
        
    def test_add(self):
        ol = OrderedStringList(True)
        ol.add("6")
        self.assertEqual(ol.values(), ["6"])
        ol.add("5")
        self.assertEqual(ol.values(), ["5", "6"])
        ol.add("4")
        self.assertEqual(ol.values(), ["4", "5", "6"])
        ol.add("7")
        self.assertEqual(ol.values(), ["4", "5", "6", "7"])
        
    def test_find(self):
        ol = OrderedStringList(True)
        ol.add("6")
        ol.add("5")
        ol.add("4")
        ol.add("7")
        self.assertEqual(ol.find("4").value, "4")
        self.assertEqual(ol.find("5").value, "5")
        self.assertEqual(ol.find("6").value, "6")
        self.assertEqual(ol.find("7").value, "7")
        self.assertEqual(ol.find("-1"), None)
        
    def test_del(self):
        ol = OrderedStringList(True)
        ol.add("6")
        ol.add("5")
        ol.add("4")
        ol.add("7")
        self.assertEqual(ol.values(), ["4", "5", "6", "7"])
        ol.delete("5")
        self.assertEqual(ol.values(), ["4", "6", "7"])
        ol.delete("7")
        self.assertEqual(ol.values(), ["4", "6"])
        ol.delete("6")        
        self.assertEqual(ol.values(), ["4"])
        ol.delete("4")
        self.assertEqual(ol.values(), [])
        
    
    def test_add_del(self):
        ol = OrderedStringList(True)
        ol.add(" string4  ")
        ol.add("  string1  ")
        ol.add("string3  ")
        ol.add("  string2")
        self.assertEqual(ol.values(), ["  string1  ", "  string2", "string3  ", " string4  "])
        ol.delete("  string2")
        self.assertEqual(ol.values(), ["  string1  ", "string3  ", " string4  "])
        ol.delete("  string3")
        self.assertEqual(ol.values(), ["  string1  ", " string4  "])
        ol.add("string2 2 ")
        self.assertEqual(ol.values(), ["  string1  ", "string2 2 ", " string4  "])
            
if __name__ == '__main__':
    unittest.main()

