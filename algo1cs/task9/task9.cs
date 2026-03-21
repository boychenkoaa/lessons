using System;
using System.Linq;

namespace AlgorithmsDataStructures
{

    public class NativeDictionary<T>
    {
        public int size;
        public string[] slots;
        public T[] values;

        public NativeDictionary(int sz)
        {
            size = sz;
            slots = new string[size];
            values = new T[size];
        }

        public int HashFun(string key)
        {
            // всегда возвращает корректный индекс слота
            return HashFunExt(key, slots);
        }

        public int HashFunExt(string key, string[] _slots)
        {
            // всегда возвращает корректный индекс слота
            if (key == "")
                return 0;
            return (key[0] + key[^1]) % _slots.Length;
        }

        public bool IsKey(string key)
        {
            // возвращает true если ключ имеется,
            // иначе false
            int candidate = SeekSlot(key, slots);
            return candidate >= 0 && slots[candidate] is not null;
        }


        private void Realloc()
        {
            int new_size = 2 * size;
            string[] new_slots = new string[new_size];
            T[] new_values = new T[new_size];
            foreach ((string k, T v) in slots.Zip(values).Where(pair => pair.First != null))
            {
                int index = PutInto(k, v, new_slots, new_values);
                if (index == -1)
                    throw new Exception("Reallocation Error: new slots array is too small"); // такого случаться не должно, зачем тогда реаллокация
            }

            size = new_size;
            slots = new_slots;
            values = new_values;
        }

        /*
        возврат место под key: один из трех вариантов
        а. индекса где он уже есть,
        б. индекса где его можно разместить
        в. -1 (если массив забит и ключа нет)

        кто по факту случился, а или б, дополнительно нужно проверять в вызывающем методе
        (в случае с Put не нужно, там в любом случае перезапись)
        с -1 все ясно
        */
        private int SeekSlot(string key, string[] _slots)
        {
            int start_index = HashFunExt(key, _slots);
            int index = start_index;
            while (_slots[index] != null && _slots[index] != key)
            {
                index = (index + 1) % _slots.Length;
                if (index == start_index)
                    return -1;
            }
            return index;
        }

        // "черновой" метод вставки, и для основного массива, и для нового 
        private int PutInto(string key, T value, string[] targetSlots, T[] targetValues)
        {
            int index = SeekSlot(key, targetSlots);
            if (index == -1)
                return -1;
            targetSlots[index] = key;
            targetValues[index] = value;
            return index;
        }

        // если места не хватило -- реаллокация
        public void Put(string key, T value)
        {
            // гарантированно записываем 
            // значение value по ключу key
            int candidate = SeekSlot(key, slots);
            if (candidate == -1) // нет места
                Realloc();
            PutInto(key, value, slots, values);
        }

        public T Get(string key)
        {
            // возвращает value для key, 
            // или null если ключ не найден
            int candidate = SeekSlot(key, slots);
            if (candidate >= 0 && slots[candidate] is not null)
                return values[candidate];
            return default(T);
        }
    }
}
