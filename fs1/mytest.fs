module MyTest

let check name input expected actual =
    let success = expected = actual
    let status = if success then "ОК" else "ERROR"

    printfn "%s" name
    printfn "вход:      %s" input
    printfn "ожидание:  %A" expected
    printfn "результат: %A" actual
    printfn "статус:    %s\n" status

    success

let multicheck groupName tests =
    printfn "\n%s" groupName

    let results =
        tests
        |> List.map (fun (name, input, expected, actual) ->
            check name input expected actual)

    let success = results |> List.forall (fun result -> result)
    let status = if success then "ОК" else "ERROR"
    printfn "статус группы: %s" status
