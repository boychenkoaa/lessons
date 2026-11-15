// 47.4.1
let f n =
    let mutable fact = 1
    let mutable i = 1
    while i <= n do
        fact <- fact * i
        i <- i + 1
    fact

// 47.4.2
let fibo n =
    let mutable current = 1
    let mutable prev = 0
    let mutable i = 1
    while i < n do
        let tmp = current
        current <- current + prev
        prev <- tmp
        i <- i+1
    if n = 0 then 0 else current
