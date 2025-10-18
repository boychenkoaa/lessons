public class BankAccount
{
    public double Balance { get; private set; }
    public BankAccount(double balance)
    {
        if (balance < 0)
        {
            throw new ArgumentException("Баланс не может быть отрицательным!");
        }

        Balance = balance;
    } 

    public void Deposit(double amount)
    {
        if (amount < 0)
        {
            throw new ArgumentException("Сумма пополнения не может быть отрицательной!");
        }
        Balance += amount;
    }

    public void WithDraw(double amount)
    {
        if (Balance < amount)
        {
            throw new ArgumentException("Сумма снятия больше текущего баланса!");
        }
        if (amount < 0)
        {
            throw new ArgumentException("Сумма снятия не может быть отрицательной");
        }
        Balance -= amount;
    }
}
