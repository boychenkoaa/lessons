// 39.1
let rec rmodd = function
    | [] -> []
    | [x] -> []
    | first :: second :: tail -> second :: rmodd tail

// 39.2
let rec del_even = function
    | [] -> []
    | first :: tail when first % 2 = 0 -> del_even tail
    | first :: tail -> first :: del_even tail


// 39.3
let rec multiplicity x = function
    | [] -> 0
    | first :: tail -> (if x = first then 1 else 0) + multiplicity x tail


// 39.4
let rec split_base = function
    | [], li_even, li_odd -> li_even, li_odd
    | [x], li_even, li_odd -> x :: li_even, li_odd
    | el0 :: el1 :: tail, li_even, li_odd -> split_base (tail, el0 :: li_even, el1 :: li_odd)

let split li =
    let (li_even, li_odd)  = split_base (li, [], [])
    List.rev li_even, List.rev li_odd


// 39.5
let rec zip = function
    | [], [] -> []
    | head1 :: tail1, head2 :: tail2 -> head1 :: head2 :: zip(tail1, tail2)
