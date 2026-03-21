using System;
using System.Collections.Generic;

/*
Рефлексия на 7 задание
9. Решено верно
10. Я понял подсписок как "упорядоченное подмножество", это упростило алгоритм, неумышленно)
Идем по "большому" списку, если совпал элемент с элементм подсписка -- двигаем индекс в подсписке.
Если в конце цикла дошли до конца подсписка вторым индексом -- значит вхождение есть.
11. Решено верно
12. Решено верно
*/

namespace AlgorithmsDataStructures
{
    /*
        простенький динамический массив, с косметическими правками предыдущих заданий
    */

    public class DynArray <T>
    {
        private T[] array;
        public int Count { get; private set; }
        private int Capacity => array.Length;

        public DynArray()
        {
            array = new T[16];
            Count = 0;
        }

        // команда: реаллокация
        // без предусловий
        // не бросает исключений, если новый размер меньше 
        private void Realloc(int new_size)
        {
            T[] new_array = new T[new_size];
            if (new_size < Count)
                throw new Exception("New size is too small");
            
            int sz = new_size < Capacity ? new_size : Capacity;
            for (int i = 0; i < sz; i++)
                new_array[i] = array[i];
            array = new_array;
        }

        // команда: вставка value на место index
        // предусловие: индекс корректен
        public void Insert(T value, int index)
        {
            if (index < 0 || index > Count)
                throw new IndexOutOfRangeException("on Insert");

            if (Count == Capacity)
                Realloc(2 * Capacity);

            for (int i = Count; i > index; i--)
                array[i] = array[i - 1];
            array[index] = value;
            Count++;
        }
       
        // команда - удаление элемента по индексу index
        // предусловие - индекс корректен
        public void Remove(int index)
        {
            if (index < 0 || index >= Count)
                throw new IndexOutOfRangeException("on Remove");
            
            // сдвиг
            for (int i = index; i < Count-1; i++)
                array[i] = array[i+1];
            Count--;
            
            // если нужно, делаем реаллокацию
            if (Count < 0.5 * Capacity)
            {
                int new_size = 3 * Capacity / 2;
                new_size = new_size < 16 ? 16 : new_size;
                Realloc(new_size);
            }

        }

        // запрос - взятие элемента по индексу index
        // предусловие - индекс корректен
        public T GetItem(int index)
        {
            if (index < 0 || index >= Count)    
                throw new IndexOutOfRangeException("on GetItem");
            return array[index];
        }

        // запрос - замена элемента по индексу index
        // предусловие - индекс корректен
        public void SetItem(int index, T value)
        {
            if (index < 0 || index >= Count)    
                throw new IndexOutOfRangeException("on SetItem");
            array[index] = value;
        }
        
    }

    /*
    упорядоченное множество -- все элементы уникальны с точки зрения Eq
    по хорошему, они должны быть Comparable
    множество базируется на динамическом массиве
    */

    public class OrderedSet<T>
    {
        private readonly DynArray<T> Arr;
        public int Count => Arr.Count;
        
        public bool Ascending {get; private set;}
        
        public OrderedSet(bool _asc = true)
        {
            Arr = new DynArray<T>();
            Ascending = _asc;
        }

        // запрос внутренний метод сравнения
        protected virtual int Compare(T v1, T v2)
        {
            // <0 если v1 < v2
            // 0 если v1 == v2
            // >0 если v1 > v2

            if (typeof(T) == typeof(String))
            {
                var s1 = v1.ToString().Trim();
                var s2 = v2.ToString().Trim();
                return s1.CompareTo(s2);
            }

            return Comparer<T>.Default.Compare(v1, v2);
        }

        // "сравнители" (предикаты) для доступа снаружи <, >, ==< <=, >=
        // учитывает Ascending
        public bool Le(T v1, T v2) => Ascending ? Compare(v1, v2) < 0 : Compare(v1, v2) > 0;
        public bool Ge(T v1, T v2) => Ascending ? Compare(v1, v2) > 0 : Compare(v1, v2) < 0;
        public bool Eq(T v1, T v2) => Compare(v1, v2) == 0;
        public bool Leq(T v1, T v2) => Le(v1, v2) || Eq(v1, v2);
        public bool Geq(T v1, T v2) => Ge(v1, v2) || Eq(v1, v2);

        public int Find(T value)
        {
            /*
            запрос: бинарный поиск элемента за логарифмическое время
            без предусловий
            возвращает индекс для вставки элемента 0..Count 
            если больше всех (с учетом ascending) -- возвращает Count
            */

            int l = -1;
            int r = Arr.Count;
            while (l < r - 1)
            {
                int m = (l + r) / 2;
                if (Le(Arr.GetItem(m), value))
                    l = m;
                else
                    r = m;
            }
            return r;
        }


        // команда: добавляем либо заменяем value
        // без предусловий
        public void Add(T value)
        {
            int index = Find(value);
            if (Has(value))
                Arr.SetItem(index, value);
            else
                Arr.Insert(value, index);
        }

        // команда: удаление элемента с индексом index
        // предусловие: индекс корректен
        public void Remove(int index)
        {
            if (!HasIndex(index))
                throw new IndexOutOfRangeException();
            Arr.Remove(index);
        }

        // запрос: корректен ли индекс
        // без предусловий
        public bool HasIndex(int index) 
        { 
            return index >=0 && index < Count;
        }

        
        // запрос: есть ли элемент
        // без предусловий
        public bool Has(T value)
        {
            int index = Find(value);
            return HasIndex(index) && Eq(value, Arr.GetItem(index));
        }

        // команда: удаление элемента
        // предусловие: элемент есть
        public void Pop(T value)
        {
            if (!Has(value))
                throw new KeyNotFoundException("Pop: value is not found");
            int index = Find(value);
            Remove(index);
        }
    
        // запрос -- взятие элемента по индексу
        // предусловие -- индекс корректен
        public T GetItem(int index)
        {
            if (!HasIndex(index))
                throw new IndexOutOfRangeException();
            return Arr.GetItem(index);
        }

    }

    // упорядоченное множество пар ключ/значение
    // сравниваются по ключу (и заменяются, соответственно, тоже)
    public class KVOrderedSet<T> : OrderedSet<(string Key, T Value)>
    {
        public KVOrderedSet(bool _asc = true) : base(_asc) { }

        protected override int Compare((string Key, T Value) v1, (string Key, T Value) v2)
        {
            string s1 = v1.Key?.Trim() ?? string.Empty;
            string s2 = v2.Key?.Trim() ?? string.Empty;
            return s1.CompareTo(s2);
        }
    }

    // словар на упорядоченном списке
    // поиск за логарифм, вставка / удаление за O(N)
    // по сути, обертывает KVOrderedSet
    public class NativeDictionary3<T>
    {
        private readonly KVOrderedSet<T> kv_set;

        public NativeDictionary3()
        {
            kv_set = new KVOrderedSet<T>(true);
        }

        public void Add(string key, T value)
        {
            kv_set.Add((key, value));
        }

        public void Remove(string key)
        {
            kv_set.Pop((key, default));
        }

        public T GetItem(string key)
        {
            (string Key, T Value) kv = (key, default);
            if (!kv_set.Has(kv))
                return default;
            int index = kv_set.Find(kv);
            return kv_set.GetItem(index).Value;
        }
    }

    /*
    словарь с использованием бинарных ключей -- ulong
    стандартные операции с ними должны быть уже битовыми, поэтому я специально нигде их не использовал
    тут я могу ошибаться, конечно, возможно все сложнее
    все методы просто дублируют методы основного словаря из task9
    */
    public class NativeDictionaryBin<T>
    {
        public int size;
        public ulong?[] slots;
        public T[] values;

        public NativeDictionaryBin(int sz)
        {
            size = sz;
            slots = new ulong?[size];
            values = new T[size];
        }

        public ulong HashFun(ulong key)
        {
            return key % (ulong)slots.Length;
        }

        public bool IsKey(ulong key)
        {
            int candidate = SeekSlot(key, slots);
            return candidate >= 0 && (slots[candidate] != null);
        }

        private void Realloc()
        {
            int new_size = 2 * size;
            ulong?[] new_slots = new ulong?[new_size];
            T[] new_values = new T[new_size];
            for (int i = 0; i < slots.Length; i++)
            {
                if (slots[i] == null)
                    continue;
                int index = PutInto(slots[i].Value, values[i], new_slots, new_values);
                if (index == -1)
                    throw new Exception("Reallocation Error: new slots array is too small");
            }

            size = new_size;
            slots = new_slots;
            values = new_values;
        }

        private int SeekSlot(ulong key, ulong?[] targetSlots)
        {
            int start_index = (int)(key % (ulong)targetSlots.Length);
            int index = start_index;
            while (targetSlots[index].HasValue && targetSlots[index].Value != key)
            {
                index = (index + 1) % targetSlots.Length;
                if (index == start_index)
                    return -1;
            }
            return index;
        }

        private int PutInto(ulong key, T value, ulong?[] targetSlots, T[] targetValues)
        {
            int index = SeekSlot(key, targetSlots);
            if (index == -1)
                return -1;
            targetSlots[index] = key;
            targetValues[index] = value;
            return index;
        }

        public void Put(ulong key, T value)
        {
            int candidate = SeekSlot(key, slots);
            if (candidate == -1)
                Realloc();
            PutInto(key, value, slots, values);
        }

        public T Get(ulong key)
        {
            int candidate = SeekSlot(key, slots);
            if (candidate >= 0 && slots[candidate].HasValue)
                return values[candidate];
            return default;
        }
    }
}
