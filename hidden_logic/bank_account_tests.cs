using Xunit;

namespace task2_tests;

public class BankAccountTests
{
    [Fact]
    public void TestBasics()
    {
        var bank_account = new BankAccount(-10);
        bank_account.Deposit(30);
        Assert.Equal(20, bank_account.Balance);
        bank_account.WithDraw(50);
        Assert.Equal(-30, bank_account.Balance);
    }
}