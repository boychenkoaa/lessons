// 17.1
let rec pow (s, n) =
    match n with
    | 0 -> ""
    | n -> s + pow(s, n - 1)


// 17.2
let rec isIthChr (s, n, c) = s.[n] = c


// 17.3
let rec occFromIth (s, n, c) =
    match n with
    | n when n >= String.Length s -> 0
    | n when s.[n] = c -> 1 + occFromIth(s, n+1, c)
    | _ -> occFromIth(s, n+1, c)
