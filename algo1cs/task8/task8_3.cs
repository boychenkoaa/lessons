
/*
Рефлексия на задание 6
6.4 (палиндром)
решено верно

6.5 (мин элемент за О(1))
решил другим способом
вместо "стека минимумов" хранил "дек минимумов" (в моем случае второй массив), с ним работать проще, но выше сложность по памяти в среднем
при добавлении в начало/в конец => во вторую деку минимальный элемент тоже добавлялся в начало / в конец (сравнение нового элемента шло и с первым, и с последним)
при удалении так же синхронно удалялся.

6.6 (дек на базе динамического массива)
Смешал функционал очереди и динамического массива (там же был еще и массив минимумов для 6.5), но понимаю что это не гуд. 
Торопился + класс же небольшой, я ленив... Правильнее конечно разделить и вкладывать.
*/

/*
1. Проектирование отсутствует как таковое, TODO переделать

2. Прогон DDOS на 60 элементов с однинаковыми хешами (хеш -- первый символ строки)
шаг = 1
размер таблицы 101
- один хеш: 3540 (почти квадратичная сложность)
- подключили вторую хеш функцию: 2176 (ожидаемо уменьшилось почти вдвое)
DDoS атака с солью
- с солью и одной хеш-функцией: 2900
*/

using System;

namespace AlgorithmsDataStructures
{
    public class DynamicHashTable
    {


        public int step;
        public string[] slots;
        public long SeeksCount { get; protected set; } = 0;

        public int Size => slots.Length;
        public int Count { get; protected set; } = 0;
        /* 
        каждое следующее простое число ~2 раза больше предыдущего
        остановимся на 1млрд элементов -- это минимум 2 гб памяти (неповторяющиеся строки...), 
        не хочу возиться с генераторами + нет смысла увеличивать до бесконечности
        */

        private readonly int[] PRIMES = { 101, 211, 431, 863, 1951, 4057,
        8123, 16333, 32687, 65521, 131561, 263129, 526271, 1052551,
        2105111, 4210247, 8420509, 16841021,
        33682067,67364153, 134728313, 269456641, 538913339, 1077826679
        };
        private int prime_index = 0;

        public DynamicHashTable(int stp = 1)
        {
            step = stp;
            slots = new string[PRIMES[prime_index]];
            for (int i = 0; i < slots.Length; i++) slots[i] = null;
        }

        public static int HashFun(string value, int size)
        {
            // всегда возвращает корректный индекс слота
            if (value.Length == 0)
                return 0;
            return value[0] % size;
        }

        public static int HashFun2(string value, int size)
        {
            // всегда возвращает корректный индекс слота
            if (value.Length == 0)
                return 0;
            return (value[0] + value[^1]) % size;
        }

        public virtual int SeekSlot(string value, string[] slots, int size)
        {
            int index = HashFun(value, size);
            if (slots[index] == value)
                return -2;
            if (slots[index] != null)
                index = HashFun2(value, size);
            if (slots[index] == value)
                return -2;
            int start_index = index;
            while (slots[index] != null)
            {
                if (slots[index] == value)
                    return -2;
                index = (index + step) % size; // тут Size использовать нельзя, тк slots это параметр
                SeeksCount++;
                if (index == start_index)
                    return -1;
            }
            
            return index;
        }

        /*
        добавлен Resize при пустом слоте
        таблица растет бесконечно
        */
        public int Put(string value)
        {
            // записываем значение по хэш-функции
            // возвращается индекс слота или -1
            // если из-за коллизий элемент не удаётся разместить 
            if (Count >= 0.7 * slots.Length)
                Resize();

            int index = SeekSlot(value, slots, slots.Length);
            if (index == -2)
                return -1;
            if (index == -1)
                Resize();
            index = SeekSlot(value, slots, slots.Length);
            if (index == -2)
                return -1;
            if (index == -1) // это вырожденный случай, если Size и Step подобраны корректно, то после реаллокации свободные места будут всегда
                return -1;
            slots[index] = value;
            Count++;
            return index;
        }

        public virtual int Find(string value)
        {
            // находит индекс слота со значением, или -1
            int index = HashFun(value, slots.Length);
            if (slots[index] != null && slots[index] != value)
                index = HashFun2(value, slots.Length);
            int start = index;
            while (slots[index] != null)
            {
                if (slots[index] == value)
                    return index;
                index = (index + step) % slots.Length;
                if (index == start)
                    break;
            }
            return -1;
        }

        /* 
        Реализация реаллокации
        При реаллокации все элементы перехешируются в новый массив
        Сложность O(n)
        Пока не вижу способа уменшить затраты по времени, кроме как использовать простые числа как новые размеры массива
        */
        private void Resize()
        {
            prime_index++;
            if (prime_index >= PRIMES.Length)
                throw new IndexOutOfRangeException("Слишком большой размер таблицы");

            int new_size = PRIMES[prime_index];
            string[] new_slots = new string[new_size];
            for (int i = 0; i < new_size; i++) new_slots[i] = null;
            Count = 0;
            for (int i = 0; i < slots.Length; i++)
            {
                if (slots[i] != null)
                {
                    int new_index = SeekSlot(slots[i], new_slots, new_size);
                    if (new_index == -1) // это перестраховка, не должен сработать никогда -- мы же только что увеличили объем!
                        throw new OverflowException("Resized table overflow");
                    new_slots[new_index] = slots[i];
                    Count++;
                }
            }
            
            slots = new_slots;
        }


        public void DDoS(string[] values)
        {
            foreach (string value in values)
                Put(value);
        }

        public string salt(string value)
        {
            return value + value.Length.ToString();
        }

        public void DDoSSalt(string[] values)
        {
            foreach (string value in values)
                Put(salt(value));
        }
    }

    public class DynamicHashTable2 : DynamicHashTable
    {

        public override int SeekSlot(string value, string[] slots, int size)
        {
            int index = HashFun(value, size);
            int start_index = index;
            while (slots[index] != null)
            {
                if (slots[index] == value)
                    return -2;
                index = (index + step) % size; // тут Size использовать нельзя, тк slots это параметр
                SeeksCount++;
                if (index == start_index)
                    return -1;
            }
            return index;
        }

        public override int Find(string value)
        {
            int index = HashFun(value, slots.Length);
            int start = index;
            while (slots[index] != null)
            {
                if (slots[index] == value)
                    return index;
                index = (index + step) % slots.Length;
                if (index == start)
                    break;
            }
            return -1;
        }
    }
}
