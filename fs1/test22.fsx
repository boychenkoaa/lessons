let rec naturals n =
    Cons(n, lazy (naturals (n + 1)))

let n0 = naturals 0

[0; 1; 10; 30000]
|> List.iter (fun n ->
    printfn "nth n0 %d = %d" n (nth n0 n))
