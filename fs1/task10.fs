(*
0 <= hours <= 11
0 <= minutes <= 59
f in {"AM", "PM"}
*)
type TimeOfDay = {hours: int; minutes: int; f:string}
let (.>.) {hours = h1; minutes = m1; f = f1}
    {hours = h2; minutes = m2; f = f2} =
    (f1, h1, m1) > (f2, h2, m2)
