#load "mytest.fs"
open MyTest

let m = Map.ofList [1, "one"; 2, "two"]

let results = [
    check "существующий ключ" "try_find 2 m" (Some "two") (try_find 2 m)
    check "отсутствующий ключ" "try_find 3 m" None (try_find 3 m)
    check "пустой Map" "try_find 1 Map.empty" None (try_find 1 (Map.empty<int, string>))
]

if not (List.forall id results) then
    exit 1
