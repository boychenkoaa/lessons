// 50.2.1
let fac_seq n = seq {
    let mutable f = 1
    yield f
    for i in 1..n do
        f <- f*i
        yield f
}

// 50.2.2
let seq_seq n = seq {
    for i in 0..n-1 do
        yield (i + i%2) / 2 * (1 - 2*(i%2))
}
