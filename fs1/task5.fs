let notDivisible (n, m) = n <> 0 && m % n = 0

let prime n =
    let rec is_del_nxt = function
        | d when d * d > n -> false
        | d -> n % d =  0 || is_del_nxt(d+1) // если делится, то рекурсия завершится из за "ленивости"
    n > 1 && not (is_del_nxt 2)
