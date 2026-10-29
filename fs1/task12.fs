let rec progression a0 d n k = if k = n then [a0+d*(n-1)] else (a0+d*(k-1)) :: progression a0 d n (k+1)

// 34.1
let upto n = progression 1 1 n 1

// 34.2
let dnto n = progression n -1 n 1

// 34.3
let evenn n = progression 0 2 n 1
