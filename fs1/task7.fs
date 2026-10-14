//module task7

// 20.3.1
let vat n x =  (1.0 + (float n) / 100.0) * x

// 20.3.2
let unvat n x = 100.0 / (100.0 + float(n)) * x

//вспомогательная для 20.3.3
let rec min_acc f n = if f(n) = 0 then n else min_acc f (n+1)

// 20.3.3
let rec min f = min_acc f 0
