// module task6

// 17.1
let rec pow (s, n) =
    match n with
    | 0 -> ""
    | n -> s + pow(s, n - 1)

// 17.2
let rec isIthChar (s, n, c) =
    n >= 0 && n < String.length s && s.[n] = c

// 17.3
let rec occFromIth (s, n, c) =
    match n with
    | n when (n < 0 || n >= String.length s) -> 0
    | n when s.[n] = c -> 1 + occFromIth(s, n+1, c)
    | _ -> occFromIth(s, n+1, c)
