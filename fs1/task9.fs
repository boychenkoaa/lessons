// конвертеры из медяков и в медяки
let c2t c =  c / 240, c % 240 / 12 ,c % 12
let t2c (g, s, c) = g*240 + s*12 + c

// 23.4.1
let (.+.) x y = c2t(t2c(x) + t2c(y))
let (.-.) x y = c2t(t2c(x) - t2c(y))

// 23.4.2

// вспомогательные
let neg (a: float, b: float) = -a, -b

let inv(a, b) =
    let r = a ** 2.0 + b**2.0
    a/r, -b/r


let (.+) x, y =
   let (a, b): float*float = x
   let (c, d): float*float = y
   a+c, b+d

let (.-) x y =
    x .+ (neg y)

let (.*) x y =
    let (a, b): float*float = x
    let (c, d): float*float = y
    (a*c, b*c) .+ (-b*d, a*d)


let (./) x y = x .* (inv  y)
