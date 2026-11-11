#load "mytest.fs"
open MyTest

multicheck "allSubsets" [
    ("все двухэлементные подмножества", "n = 3, k = 2", set [set [1;2]; set [1;3]; set [2;3]], allSubsets 3 2)
    ("пустое подмножество", "n = 3, k = 0", set [Set.empty<int>], allSubsets 3 0)
    ("k больше n", "n = 3, k = 4", Set.empty<Set<int>>, allSubsets 3 4)
]
