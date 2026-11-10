// мне не нравится это решение,
// оно имитирует генераторы и итеративный подсчет
// а не испльзует рекуррентные соотношения

// следующее множество в ЛГ-порядке
let rec nxt = function
    | m,acc,[] -> None
    | m,acc,h::t when h = m -> nxt(m-1,acc+1,t)
    | m,acc,h::t when h <> m -> Some([h+acc+1 .. -1 .. h+2] @ ((h+1) :: t))

let rec all_subsets_base n current result =
    match nxt(n,0,current) with
        | None -> current::result
        | Some subset -> all_subsets_base n subset (current::result)


let allSubsets n k =
