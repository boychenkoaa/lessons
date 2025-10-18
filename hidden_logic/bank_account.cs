public class BankAccount
{
    public double Balance { get; private set; }
    public BankAccount(double balance) => Balance = balance;

    public void Deposit(double amount)
    {
        Balance += amount;
    }

    public void WithDraw(double amount)
    {
        Balance -= amount;
    }
}