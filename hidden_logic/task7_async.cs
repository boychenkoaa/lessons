using System;
using System.Threading;
using System.Threading.Tasks;

/*
7 способов просуммировать прогрессию от 1 до N
- без синхронизации
- мьютекс
- атомарный инкремент
- семафор
- rw-lock
- события
- таски
*/


// Базовый класс для всех калькуляторов
public abstract class BaseProgressionCalculator
{
    protected int N;
    protected Thread[] threads;
    protected int Count { get; set; }

    public BaseProgressionCalculator(int N)
    {
        this.N = N;
        this.Count = 0;
        this.threads = new Thread[N];
    }

    protected void IncrementNTimes(int n, Action incrementAction)
    {
        for (int i = 0; i < n; i++)
        {
            incrementAction();
        }
    }

    public abstract void Calculate();
}

// Без синхронизации (race condition)
public class UnsafeProgressionCalculator : BaseProgressionCalculator
{
    public UnsafeProgressionCalculator(int N) : base(N) { }

    public override void Calculate()
    {
        for (int i = 0; i < N; i++)
        {
            Count += i;
        }
    }
}

// С использованием мьютекса
public class MutexProgressionCalculator : BaseProgressionCalculator
{
    private static Mutex mutex = new Mutex();

    public MutexProgressionCalculator(int N) : base(N) { }

    private void CounterIncrement()
    {
        mutex.WaitOne();
        Count++;
        mutex.ReleaseMutex();
    }

    public override void Calculate()
    {
        for (int i = 0; i < N; i++)
        {
            threads[i] = new Thread(() => IncrementNTimes(i, CounterIncrement));
        }

        for (int i = 0; i < N; i++)
        {
            threads[i].Start();
        }

        for (int i = 0; i < N; i++)
        {
            threads[i].Join();
        }
    }
}

// С использованием атомарных операций
public class AtomicProgressionCalculator : BaseProgressionCalculator
{
    public AtomicProgressionCalculator(int N) : base(N) { }

    private void CounterIncrement()
    {
        Interlocked.Increment(ref Count);
    }

    public override void Calculate()
    {
        for (int i = 0; i < N; i++)
        {
            threads[i] = new Thread(() => IncrementNTimes(i, CounterIncrement));
        }

        for (int i = 0; i < N; i++)
        {
            threads[i].Start();
        }

        for (int i = 0; i < N; i++)
        {
            threads[i].Join();
        }
    }
}

/*
С использованием семафора
ограничение искуственное, но тем не менее
*/
public class SemaphoreProgressionCalculator : BaseProgressionCalculator
{
    private const int MAX_THREADS = 10;
    private static Mutex mutex = new Mutex();

    public SemaphoreProgressionCalculator(int N) : base(N) { }

    private void CounterIncrement()
    {
        mutex.WaitOne();
        Count++;
        mutex.ReleaseMutex();
    }

    public override void Calculate()
    {
        Semaphore semaphore = new Semaphore(MAX_THREADS, MAX_THREADS);

        for (int i = 0; i < N; i++)
        {
            threads[i] = new Thread(() =>
            {
                semaphore.WaitOne();
                try
                {
                    IncrementNTimes(i, CounterIncrement);
                }
                finally
                {
                    semaphore.Release();
                }
            });
        }

        for (int i = 0; i < MAX_THREADS; i++)
        {
            threads[i].Start();
        }

        for (int i = 0; i < MAX_THREADS; i++)
        {
            threads[i].Join();
        }
        Console.WriteLine($"Count: {Count}");
    }
}

/*
rw lock
суммирование идет через массив, но в один элемент массива могут писать несколько потоков
надо его блочить на время инкремента
*/
public class ReaderWriterProgressionCalculator : BaseProgressionCalculator
{
    private static ReaderWriterLockSlim rwLock = new ReaderWriterLockSlim();
    private int[] summands;
    private const int ARRAY_SIZE = 5;

    public ReaderWriterProgressionCalculator(int N) : base(N)
    {
        this.summands = new int[ARRAY_SIZE];
    }

    // блочим массив на время инкремента
    private void IncrementArrayElement(int index)
    {
        rwLock.EnterWriteLock();
        try
        {
            summands[index]++;
        }
        finally
        {
            rwLock.ExitWriteLock();
        }
    }

    public override void Calculate()
    {
        for (int i = 0; i < N; i++)
        {
            int threadIndex = i;
            threads[i] = new Thread((int n) =>
            {
                int arrayIndex = threadIndex % ARRAY_SIZE;
                for (int j = 0; j < n; j++)
                {
                    IncrementArrayElement(arrayIndex);
                }
            });
        }

        for (int i = 0; i < N; i++)
        {
            threads[i].Start(i);
        }

        for (int i = 0; i < N; i++)
        {
            threads[i].Join();
        }

        int Count = summands.Sum();
        Console.WriteLine($"Count: {Count}");
    }


}

/*
события
уведомление о завершении -- через события
*/
public class EventProgressionCalculator : BaseProgressionCalculator
{
    private static AutoResetEvent calculationDone = new AutoResetEvent(false);
    private static bool isCalculating = false;

    public EventProgressionCalculator(int N) : base(N) { }

    public override void Calculate()
    {
        isCalculating = true;

        // поток для консоли
        Thread consoleThread = new Thread(() =>
        {
            // Просто ждем завершения вычислений
            calculationThread.WaitOne();
            Console.WriteLine($"Вычисления завершены! Count: {Count}");
        });

        // поток для вычислений
        Thread calculationThread = new Thread(() =>
        {
            for (int i = 0; i < N; i++)
            {
                Count += i;
            }

            isCalculating = false;
            calculationDone.Set();
        });

        // погнали
        consoleThread.Start();
        calculationThread.Start();
        calculationThread.Join();
        consoleThread.Join();
    }
}

/*
таски, удобно
стандартный async / await
*/
public class TaskProgressionCalculator : BaseProgressionCalculator
{
    public TaskProgressionCalculator(int N) : base(N) { }

    public override void Calculate()
    {
        CalculateAsync().Wait();
    }

    private async Task CalculateAsync()
    {
        // таск для вычислений
        Task calculationTask = Task.Run(async () =>
        {
            for (int i = 0; i < N; i++)
            {
                Count += i;
            }
        });

        // ждем завершения вычислений
        await calculationTask;

        // печатаем результат
        Console.WriteLine($"Вычисления завершены! Count: {Count}");
    }
}
