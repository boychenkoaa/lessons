namespace T5_2;
using Xunit;

public class Task5p2Tests
{
    [Theory]
    [InlineData(new int[] { }, double.NaN, AverageCalculatorNew.STATUS_ERR)]
    [InlineData(null, double.NaN, AverageCalculatorNew.STATUS_ERR)]
    [InlineData(new int[] { 10, int.MaxValue - 5 }, double.NaN, AverageCalculatorNew.STATUS_ERR)]
    [InlineData(new int[] { 10, -5 }, double.NaN, AverageCalculatorNew.STATUS_ERR)]
    [InlineData(new int[] { 1, 2 }, 1.5, AverageCalculatorNew.STATUS_OK)]
    public void TestEdgeCases(int[] array, double expected_value, int expected_status)
    {
        var calculator = new AverageCalculatorNew();
        double actual_value = calculator.calculateAverage(array);
        int actual_status = calculator.CALC_AVERAGE_STATUS;

        Assert.Equal(expected_value, actual_value);
        Assert.Equal(expected_status, actual_status);
    }
}
