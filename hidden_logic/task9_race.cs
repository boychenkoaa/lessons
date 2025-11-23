using System;
using System.Threading;

public class ThreadExample
{
    private static int counter = 0;

    public static void Main(string[] args)
    {
        Action task = () =>
        {
            for (int i = 0; i < 1000; i++)
            {
                // инкремент делаем атомарным -- проблема уходит
                Interlocked.Increment(ref counter);
            }
        };

        Thread thread1 = new Thread(new ThreadStart(task));
        Thread thread2 = new Thread(new ThreadStart(task));

        thread1.Start();
        thread2.Start();

        try
        {
            thread1.Join();
            thread2.Join();
        }
        catch (ThreadInterruptedException e)
        {
            Console.WriteLine(e);
        }

        Console.WriteLine("Counter: " + counter);
    }
}
