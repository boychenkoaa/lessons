using System.Reflection;
using Xunit;

namespace task2_tests;

public class BankAccountTests
{
    [Fact]
    public void TestBasics()
    {
        Assert.Throws<ArgumentException>(() => new BankAccount(-10));
        var bank_account = new BankAccount(10);
        bank_account.Deposit(30);
        Assert.Throws<ArgumentException> (() => bank_account.Deposit(-30));
        Assert.Equal(40, bank_account.Balance);
        Assert.Throws<ArgumentException>(() => bank_account.WithDraw(50));
        Assert.Throws<ArgumentException>(() => bank_account.WithDraw(-50));
        bank_account.WithDraw(15);
        Assert.Equal(25, bank_account.Balance);
    }
}
