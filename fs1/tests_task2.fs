module Task2Tests

open Xunit
open task2

[<Theory>]
[<InlineData(0, 5)>]
[<InlineData(5, 10)>]
[<InlineData(-3, 2)>]
let test_g n ans =
    Assert.Equal(ans, g n)

[<Fact>]
let test_h () =
    Assert.Equal(5.0, h (3.0, 4.0), 3)
