// 40.1
let sum (p, xs) =
    let rec sum_acc = function
        | [], acc -> acc
        | head::tail, acc -> sum_acc (tail, acc + (if (p head) then head else 0))
    sum_acc(xs, 0)

// 40.2
// операции с мультимножествами

// 40.2.1 - количество
let rec count (xs, n) =
    let rec count_base (xs, counter) =
        match xs with
        | [] -> counter
        | head :: tail ->
            if head > n then counter
            elif head = n then count_base(tail, counter+1)
            else count_base(tail, counter)

    count_base (xs, 0)


// 40.2.2 - вставка
// перекладываем из левого в правый по 1 элементу,
// пока голова левого не станет больше n, либо он не опустеет
// сложность O(n)
let rec insert (xs, n) =
    let rec insert_base = function
        | [], right -> (List.rev right @ [n])
        | h::t, right when h >= n -> (List.rev right) @ (n::h::t)
        | h::t, right -> insert_base (t, h::right)
    insert_base (xs, [])

// 40.2.3 - пересечение
// два индекса в рекурсивном исполнении)
let rec intersect (xs1, xs2) =
    let rec intersect_base = function
        | [], xs2, ans -> List.rev ans
        | xs1, [], ans -> List.rev ans
        | h1::t1, h2::t2, ans ->
            if h1 = h2 then intersect_base(t1, t2, h1::ans)
            elif h1 < h2 then intersect_base(t1, h2::t2, ans)
            else intersect_base(h1::t1, t2, ans)
    intersect_base(xs1, xs2, [])

// 40.2.4 - объединение
// ans - перевернутый хвост результата, перед возвратом реверсируем
// меньший из h1 и h2 приписываем к ans и убираем из соответствующего списка
let rec plus (xs1, xs2) =
    let rec plus_base = function
        | [], xs2, ans -> List.rev ans @ xs2
        | xs1, [], ans -> List.rev ans @ xs1
        | h1::t1, h2::t2, ans when h1 <= h2 -> plus_base (t1, h2::t2, h1::ans)
        | h1::t1, h2::t2, ans -> plus_base (h1::t1, t2, h2::ans)
    plus_base(xs1, xs2, [])

// 40.2.5 - разность
// ans - переревернутый хвост результата, реверс перед возвратом
// если равны, то удаляем оба,
// если h1 меньше то двигаем h2,
// если h2 меньше то двигаем h1 с записью в ans
let rec minus (xs1, xs2) =
    let rec minus_base = function
        | [], xs2, ans -> List.rev ans
        | xs1, [], ans -> List.rev ans @ xs1
        | h1::t1, h2::t2, ans when h1 = h2 -> minus_base (t1, t2, ans)
        | h1::t1, h2::t2, ans when h1 < h2 -> minus_base (t1, h2::t2, h1::ans)
        | h1::t1, h2::t2, ans -> minus_base (h1::t1, t2, ans)
    minus_base(xs1, xs2, [])

// 40.3.1
// минимум
let rec smallest xs =
    let rec smallest_base = function
        | [], ans -> Some(ans)
        | h::t, ans -> smallest_base (t, if h < ans then h else ans)
    match xs with
        | [] -> None
        | h::t -> smallest_base(t, h)

// 40.3.2
// удаление
let rec delete (n, xs) =
    let rec delete_base = function
        | [], ans -> List.rev ans
        | h::t, ans when h = n -> List.rev ans @ t
        | h::t, ans -> delete_base(t, h::ans)
    delete_base (xs, [])

// 40.3.3
// сортировка
let rec sort s =
    match smallest s with
        | Some minimum -> minimum::sort(delete(minimum, s))
        | None -> []

// 40.4
let rec revrev xs =
    let rec revrev_base = function
        | [], ans -> ans
        | h::t, ans -> revrev_base (t, List.rev h :: ans)

    revrev_base (xs, [])
