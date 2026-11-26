// 50.2.1
let fac_seq n = seq {
    let mutable f = 1
    let mutable i = 0
    while true do
        yield f
        i <- i + 1
        f <- f * i
}

// 50.2.2
let seq_seq n = seq {
    let mutable i = 0
    while true do
        yield (i + i % 2) / 2 * (1 - 2 * (i % 2))
        i <- i + 1
}
