namespace Example1.Tests;
using Xunit;

public class Task5Test
{
    [Theory]
    [InlineData(new int[] { 1, 2, 3, 4, 5 }, 3.0)]
    [InlineData(new int[] { 10, 20, 30, 40, 50 }, 30.0)]
    [InlineData(new int[] { 100, 200, 300, 400, 500 }, 300.0)]
    [InlineData(new int[] { }, 0.0)] // ошибка -- деление на ноль

    public void test_calculate_average(int[] numbers, double expected)
    {
        T5.AverageCalculator calculator = new();
        double average = calculator.calculateAverage(numbers);
        Assert.Equal(average, expected);
    }

}
