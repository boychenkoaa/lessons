namespace Task4.Tests;
using Xunit;

public class Task4Test
{
    [Theory]
    [InlineData(41.0, 5.0)]
    [InlineData(50.0, 10.0)]
    [InlineData(230.0, 110.0)]

    public void test_to_celsius(double c, double expected)
    {
        Task4 task4 = new();
        double f = task4.ToCelsius(c);
        Assert.Equal(f, expected);
    }

}

public class Task5Test
{
    [Theory]
    [InlineData(new int[] { 1, 2, 3, 4, 5 }, 3.0)]
    [InlineData(new int[] { 10, 20, 30, 40, 50 }, 30.0)]
    [InlineData(new int[] { 100, 200, 300, 400, 500 }, 300.0)]
    [InlineData(new int[] { }, 0.0)] // ошибка -- деление на ноль

    public void test_calculate_average(int[] numbers, double expected)
    {
        AverageCalculator calculator = new();
        double average = calculator.calculateAverage(numbers);
        Assert.Equal(average, expected);
    }

}
