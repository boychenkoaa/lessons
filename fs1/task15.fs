// 41.4.1
let list_filter f xs = List.foldBack (fun head tail -> if f head then head::tail else tail ) xs []


// 41.4.2
let sum (p, xs) = List.fold (fun a b -> (if p b then b else 0) + a ) 0 xs

// 41.4.3
let revrev xs =
   let rev lst = List.fold (fun head tail -> tail::head) [] lst
   List.fold (fun acc lst -> rev lst :: acc) [] xs
