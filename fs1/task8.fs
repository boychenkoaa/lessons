// module Task8

// эти развернутые версии сам написал в лоб. лаконичные жпт подсказала

let curry  (f: int * int -> int) : int -> int -> int =
    let g x =
        let h y = f (x, y)
        h
    g

let uncurry (g: int -> int -> int) : int * int -> int =
    let f (x,y) =
        let h = g x
        h y
    f
