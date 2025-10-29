/*
состояние гонки возникает из-за "перемешивания" "атомарных" действий разных потоков (процессорных инструкций), 
из которых состоит инкремент: чтение, прибавление 1, запись

пример: чтение (поток 1), чтение (поток 2), инкремент (поток 1), инкремент (поток2), запись (поток 1), запись (поток 2)
ожидается увеличение на 2, по факту увеличение на 1

решение: простое -- обернуть инкремент в критическую секцию (правда, тогда нет выигрыла по сравнению с 1 потоком, но суммирует -- верно :)
классическое (ниже) -- правильно разделить состояние между потоками (каждый поток увеличивает свою переменную, в конце они суммируются)
*/

public class RaceConditionExampleFixed
{
    private static int counter = 0;

    public static int sum_fixed(int numberOfThreads, int iterations)
    {
        Thread[] threads = new Thread[numberOfThreads];
        int[] thread_sum = new int[numberOfThreads];
        for (int i = 0; i < numberOfThreads; i++)
        {
            threads[i] = new Thread(() =>
            {
                for (int j = 0; j < iterations; j++)
                {
                    thread_sum[i]++;
                }
            });
            threads[i].Start();
        }

        for (int i = 0; i < numberOfThreads; i++)
        {
            try
            {
                threads[i].Join();
            }
            catch (ThreadInterruptedException e)
            {
                Console.WriteLine(e.Message);
            }
        }
        counter = thread_sum.Sum();
        return counter
    }
}

/* 
Взаимная блокировка возникает при одновременном входе каждого из потоков 
в критическую секцию верхего уровня.
Исправления зависят от контекста, если цель -- дойти до финиша (программа полностью выполнена), 
то можно, например, поменять местами lock1 и lock2  у второго потока)
*/

public class DeadLockExampleFixed()
{
    public static void Main(string[] args)
    {
        Thread thread1 = new Thread(() =>
        {
            lock (lock1)
            {
                Console.WriteLine("Thread 1 acquired lock1");

                try { Thread.Sleep(50); }
                catch (ThreadInterruptedException e) { Console.WriteLine(e.Message); }

                lock (lock2)
                {
                    Console.WriteLine("Thread 1 acquired lock2");
                }
            }
        });

        Thread thread2 = new Thread(() =>
        {
            lock (lock1)
            {
                Console.WriteLine("Thread 2 acquired lock1");

                try { Thread.Sleep(50); }
                catch (ThreadInterruptedException e) { Console.WriteLine(e.Message); }

                lock (lock2)
                {
                    Console.WriteLine("Thread 2 acquired lock2");
                }
            }
        });

        thread1.Start();
        thread2.Start();

        try
        {
            thread1.Join();
            thread2.Join();
        }
        catch (ThreadInterruptedException e)
        {
            Console.WriteLine(e.Message);
        }

        Console.WriteLine("Finished");
    }
}
