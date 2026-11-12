// 43.3
let try_find key m =
    let rec try_find_li = function
        | _, [] -> None
        | key, (k, v)::_ when k = key -> Some v
        | key, _::t -> try_find_li (key, t)
    try_find_li (key, Map.toList m)
