// 49.5.1
let even_seq = Seq.initInfinite(fun i -> i*2+2)

// 49.5.2
// последовательность факториалов начиная с 0!
let fac_seq n = Seq.ofList(
    List.rev
        (List.fold
            (fun (h::t) m -> (m*h)::h::t)
            [1]
            [1..n]
        )
)

// 49.5.3
let seq_seq = Seq.initInfinite(fun n -> (n + n%2) / 2 * (1 - 2*(n%2)))
