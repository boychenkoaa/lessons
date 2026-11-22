let n = 7

printfn "even_seq: первые %d элементов = %A" n (even_seq |> Seq.take n |> Seq.toList)
printfn "fac_seq: факториалы от 0! до %d! = %A" n (fac_seq n |> Seq.toList)
printfn "seq_seq: первые %d элементов = %A" n (seq_seq |> Seq.take n |> Seq.toList)
