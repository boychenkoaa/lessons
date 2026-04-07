using System;
using System.Collections;
using System.Collections.Generic;

/*
рефлексия на 10 и 11
10.4 (декартово произведение) решено верно, но не обобщал на N множеств, сделано только для двух

10.5 (мульти-множество) решено верно

11.2 (слияние фильтров Блума) решено верно, слияние делал для фильтров с удалением (там не логическое сложение, а обычное)
и вероятность ложных срабатывание увеличивается

11.4 (восстановление исходного множества) реализации нет, сформулировал общий подход
ход мыслей был верный -- брут-форс по наборам слов из словаря с оптимизацией функции расстояния L1 между полученным значением и эталоном
для избегания "застреваний" алгоритмов оптимизации в локальных минимумах используем случайный поиск...
*/

/*
для задания 12 (кэш)

- Для вытеснения в кэше хранение цепочек мне видится сильно более удобным, чем пробирование. 
По производительности также не будет уступать при прочих равных (не 100% гарантия, но тем не менее).

- описание самой структуры: 
- - KVH -- иммутабельная внутренняя структура (string key, T value, int hit).
- - В хеш таблице Chains будут храниться цепочки -- списки List<KVH> у которых хеш ключа равен индексу
- - хеш функция для простоты тестирования возвращает нулевой символ строки

- для простоты тестирования все поля -- публичные

- сравнение значений вынес в метод Eq
*/

namespace AlgorithmsDataStructures
{
    public class NativeCache<T>
    {
        public readonly struct KVH
        {
            public readonly string Key;
            public readonly T Value;
            public readonly int Hit;

            public KVH(string key, T value, int hit)
            {
                Key = key;
                Value = value;
                Hit = hit;
            }
        }

        public int HashFun(string s) => string.IsNullOrEmpty(s) ? 0 : s[0] % TABLE_SIZE;

        public static bool Eq(T t1, T t2) => EqualityComparer<T>.Default.Equals(t1, t2);

        public const int TABLE_SIZE = 255;
        public int Count = 0;
        public int MaxCount;
        public List<KVH>[] Chains = new List<KVH>[TABLE_SIZE];

        public NativeCache(int max_count)
        {
            MaxCount = max_count;
            for (int i = 0; i < TABLE_SIZE; i++)
                Chains[i] = new List<KVH>();
        }

        public bool HasKey(string key)
        {
            // запрос -- проверка на вхождение ключа
            // предусловий нет
            int bucket = HashFun(key);
            var chain = Chains[bucket];
            foreach (KVH entry in chain)
                if (entry.Key == key)
                    return true;

            return false;
        }

        public bool HasValue(T value)
        {
            // запрос -- проверка на вхождение значения
            // предусловий нет
            foreach (List<KVH> chain in Chains)
                foreach (KVH entry in chain)
                    if (Eq(entry.Value, value))
                        return true;
            return false;
        }

        public T Get(string key)
        {
            /*
                запрос, ключ => значение
                предусловие -- ключ есть (иначе default)
            */
            int bucket = HashFun(key);
            var chain = Chains[bucket];
            for (int i = 0; i < chain.Count; i++)
            {
                var entry = chain[i];
                if (entry.Key == key)
                {
                    chain[i] = new KVH(entry.Key, entry.Value, entry.Hit + 1);
                    return entry.Value;
                }
            }

            return default;
        }


        private (int Bucket, int Index) GetLeastFrequentIndices()
        {
            /*
                запрос -- поиск 2х индексов самого непопулярного значения 
                возвращает пару (bucket, index)
                bucket -- номер цепочки
                index -- номер entry в цепочке
                либо (-1, -1), если таблица пуста
                предусловий нет
            */

            int bucket = -1;
            int index = -1;
            int minHit = int.MaxValue;

            // идем по таблице
            // foreach использовать не можем, нужны индексы как результат
            for (int b = 0; b < TABLE_SIZE; b++)
            {
                var chain = Chains[b];
                // идем по цепочке
                for (int i = 0; i < chain.Count; i++)
                    if (chain[i].Hit < minHit)
                    {
                        minHit = chain[i].Hit;
                        bucket = b;
                        index = i;
                    }
            }

            return (bucket, index);
        }

        public T PopLeastFrequent()
        {
            if (Count == 0)
                return default;


            var least_frequent_indices = GetLeastFrequentIndices();
            int bucket = least_frequent_indices.Bucket;
            int index = least_frequent_indices.Index;

            // перестраховка (сработает только для пустого массива, который мы исключили в начале), 
            // но пусть будет
            if (bucket < 0)
                return default;

            var chain = Chains[bucket];

            // резервим перед удалением для возврата value
            var ans = chain[index].Value;

            // удаляем
            chain.RemoveAt(index);
            Count--;

            return ans;
        }

        public T Pop(string key)
        {
            /*
            запрос и команда:
            удаление по ключу
            возвращает значение или нулл, если ключа не было
            */
            int bucket = HashFun(key);
            var chain = Chains[bucket];
            for (int i = 0; i < chain.Count; i++)
            {
                if (chain[i].Key != key)
                    continue;

                var value = chain[i].Value;
                chain.RemoveAt(i);
                Count--;
                return value;
            }

            return default;
        }

        public void Push(string key, T value)
        {
            /*
            команда - добавление в таблицу
            если превышен max_count, то вытесняется самый невостребованный
            */
            int bucket = HashFun(key);
            var chain = Chains[bucket];

            for (int i = 0; i < chain.Count; i++)
            {
                var entry = chain[i];
                if (entry.Key != key)
                    continue;

                chain[i] = new KVH(entry.Key, value, entry.Hit + 1);
                return;
            }

            if (Count >= MaxCount)
                PopLeastFrequent();

            Chains[bucket].Add(new KVH(key, value, 1));
            Count++;
        }
    }


}