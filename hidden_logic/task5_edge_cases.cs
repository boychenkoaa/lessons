namespace T5_2
{
    public class AverageCalculatorNew
    {
        public const int STATUS_NIL = 0;
        public const int STATUS_ERR = 1;
        public const int STATUS_OK = 2;

        public int CALC_AVERAGE_STATUS { get; private set; } = STATUS_NIL;

        public double calculateAverage(int[] numbers)
        {
            if (numbers == null || numbers.Length == 0)
            {
                CALC_AVERAGE_STATUS = STATUS_ERR;
                return double.NaN;
            }
            int sum = 0;
            foreach (int number in numbers)
            {
                if (number < 0 || number >= int.MaxValue - sum)
                {
                    CALC_AVERAGE_STATUS = STATUS_ERR;
                    return double.NaN;
                }
                sum += number;
            }

            // до этого момента все краевые случаи обработаны
            CALC_AVERAGE_STATUS = STATUS_OK;
            return (double)sum / numbers.Length;
        }
    }
}
