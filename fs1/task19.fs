let rec fibo1 n n1 n2 =
    if n = 0 then n2
    else fibo1 (n-1) (n1+n2) n1

let rec fibo2 n c =
    if n = 1 then c 0 1
    else fibo2 (n-1) (fun a b -> c b (a+b))

let rec bigList n k =
  if n=0 then k []
  else bigList (n-1) (fun res -> k(1::res))
