using System;
using System.Threading;

/*
не уверен, что я правильно понял задание
во всяком случае мой код значительно проще предлагаемого,
по крайней мере для восприятия)
*/

public class ComplexMultiThreadProcessingFixed
{
    private const int SIZE = 1000000;
    private static readonly int[] data = new int[SIZE];
    private static volatile int sum = 0;

    public static void Run(string[] args)
    {
        Random random = new Random();
        for (int i = 0; i < SIZE; i++)
        {
            data[i] = random.Next(100);
        }

        sum = data.AsParallel().Sum()
        Console.WriteLine("Sum of all elements: " + sum);
    }
}
