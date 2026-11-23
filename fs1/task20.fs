// 49.5.1
let even_seq = Seq.initInfinite(fun i -> i*2+2)

// 49.5.2
// последовательность факториалов начиная с 0!
let fac_seq =
    let rec factorial n =
        if n = 0 then 1
        else n * factorial (n - 1)

    Seq.initInfinite factorial

// 49.5.3
let seq_seq = Seq.initInfinite(fun n -> (n + n%2) / 2 * (1 - 2*(n%2)))
