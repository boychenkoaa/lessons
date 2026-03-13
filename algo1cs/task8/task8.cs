using System;
using System.Collections;

namespace AlgorithmsDataStructures
{
    public class HashTable
    {
        public int size;
        public int step;
        public string[] slots;

        public HashTable(int sz, int stp)
        {
            size = sz;
            step = stp;
            slots = new string[size];
            for (int i = 0; i < size; i++) slots[i] = null;
        }

        public int HashFun(string value)
        {
            // всегда возвращает корректный индекс слота
            if (value.Length == 0)
                return 0;
            return value[0] % size;
        }

        public int SeekSlot(string value)
        {
            // находит индекс пустого слота для значения, или -1
            int index = HashFun(value), start_index = index;

            while (slots[index] != null)
            {
                index = (index + step) % slots.Length;
                if (index == start_index)
                    return -1;
            }

            return index;
        }

        public int Put(string value)
        {
            // записываем значение по хэш-функции
            int index = SeekSlot(value);
            if (index == -1)
                return -1;
            slots[index] = value;
            // возвращается индекс слота или -1
            // если из-за коллизий элемент не удаётся разместить 
            return index;
        }

        public int Find(string value)
        {
            // находит индекс слота со значением, или -1
            int index = HashFun(value);
            int start = index;
            while (slots[index] != null)
            {
                if (slots[index] == value)
                    return index;
                index = (index + step) % size;
                if (index == start)
                    break;
            }
            return -1;
        }
    }
}