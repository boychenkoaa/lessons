
namespace T5
{
     public class AverageCalculator 
    {
        public void Run()
        {
            
        }

        public double calculateAverage(int[] numbers)
        {
            // деление на ноль специально не рассматриваем
            int sum = 0;
            foreach (int number in numbers)
            {
                sum += number;
            }
            
            // тут будет ошибка, если массив пустой
            return (double)sum / numbers.Length;
        }
    }

}
