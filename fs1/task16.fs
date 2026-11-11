(*
// итеративное решение через генераторы придумал сам
// дает следующее множество в ЛГ-порядке
let rec nxt = function
    | m,acc,[] -> None
    | m,acc,h::t when h = m -> nxt(m-1,acc+1,t)
    | m,acc,h::t when h <> m -> Some([h+acc+1 .. -1 .. h+2] @ ((h+1) :: t))

let rec all_subsets_base n current result =
    match nxt(n,0,current) with
        | None -> current::result
        | Some subset -> all_subsets_base n subset (current::result)
*)

// рекуррентное соотношение сначала придумал громоздкое
// ии подсказал красивое -- такие подмножества не пересекаются
let rec allSubsets n k =
    if k = 0 then set [Set.empty]
    elif k > n then Set.empty
    else Set.union
            (allSubsets (n-1) k)
            (Set.map (fun s -> Set.union (set [n]) s) (allSubsets (n-1) (k-1)))
