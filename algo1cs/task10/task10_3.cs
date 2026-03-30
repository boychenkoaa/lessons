/*
Рефлексия на задание 8
3. Не исплользовал композицию, но исключительно для скорости реализации 
+ реаллокация все равно совмещена с рехешированием

5. В целом, решено верно. 
Вместо явного значения пары (значение, соль) использовал конкатенацию строк значение+соль.
Соль задавал как функцию (обратимую). 
*/

using System;
using System.Collections.Generic;

namespace AlgorithmsDataStructures
{

    public class PowerSet3<T>: PowerSet<T>
    {
        /*
        декартово произведение
        */
        public static PowerSet<(U, V)> CartesianProduct<U, V>(PowerSet<U> a, PowerSet<V> b)
        {
            PowerSet<(U, V)> ans = new();
            foreach(U u in a.GetActiveSlots())
            {
                foreach (V v in b.GetActiveSlots())
                {
                    ans.Put((u, v));
                }
            }
            return ans;
        }

        /*
        пересечение произвольного количества множеств
        */
        public static PowerSet<T> MultiIntersection(PowerSet<T>[] sets)
        {
            int N = sets.Length ;
            if (N == 0)
                return new();
            PowerSet<T> ans = new();
            foreach(T slot in sets[0].GetActiveSlots())
                ans.Put(slot);
             
            foreach (PowerSet<T> set in sets[1..])
                ans = ans.Intersection(set);
            
                       
            return ans;
        }

    }
    /*
    множество с повторениями
    отличается от исходного только структурой массива
    вместо состояний -- количества элементов
    */
    public class Bag<T>
    {
        private int HashFun(T value)
        {
            int hash = value?.GetHashCode() ?? 0;
            int ans = (hash & 0x7fffffff) % Capacity;
            return ans;
        }

        private static bool Eq(T v1, T v2)
        {
            return EqualityComparer<T>.Default.Equals(v1, v2);
        }

        private const int Capacity = 20000;
        private T[] Slots = new T[Capacity];
        private int[] Counts = new int[Capacity];
        private int Sz;

        private int SeekSlot(T value)
        {
            /*
            возвращает, с учетом статусов:
            индекс value если он есть 
            индекс первого пустого места, если value нет (в том числе помеченного как )
            -1 если полностью заполнен и value нет
            */
            int firstDeletedIndex = -1;
            int index = HashFun(value), start_index = index;

            while (Counts[index] != 0 &&
                   !(Counts[index] > 0 && Eq(Slots[index], value)))
            {
                // обновляем firstDeletedIndex
                if (Counts[index] == -1 && firstDeletedIndex == -1)
                    firstDeletedIndex = index;

                // основной шаг
                index = (index + 1) % Slots.Length;

                // если вернулись в начало -- все заполнено
                if (index == start_index)
                    return firstDeletedIndex;
            }


            if (Counts[index] > 0) // нашли value
                return index;
            // если "мертвых" слотов не было -- вернем первый пустой, иначе первый "мертвый"
            return firstDeletedIndex == -1 ? index : firstDeletedIndex;
        }

        public Bag()
        {
            // ваша реализация хранилища
            Sz = 0;
        }

        public int Size()
        {
            // количество элементов в множестве
            return Sz;
        }

        public (T[] Values, int[] Counts) GetActiveSlots()
        {
            int activeCount = 0;
            for (int i = 0; i < Slots.Length; i++)
            {
                if (Counts[i] > 0)
                    activeCount++;
            }
            T[] values = new T[activeCount];
            int[] counts = new int[activeCount];
            int j = 0;
            for (int i = 0; i < Slots.Length; i++)
            {
                if (Counts[i] > 0)
                {
                    values[j] = Slots[i];
                    counts[j] = Counts[i];
                    j++;
                }
            }
            return (values, counts);
        }

        public bool IndexInRange(int index) => index > -1 && index < Slots.Length;
        public void Put(T value)
        {
            /*
            команда: положить элемент во множество
            */
            int index = SeekSlot(value);
            if (!IndexInRange(index))
                return;

            if (Counts[index] > 0)
            {
                Counts[index]++;
                Sz++;
                return;
            }

            Slots[index] = value;
            Counts[index] = 1;
            Sz++;
        }

        public bool Has(T value)
        {
            return GetCountOf(value) > 0;
        }

        public int GetCountOf(T value)
        {
            // возвращает количество value во множестве
            int index = SeekSlot(value);

            // если не нашли -- количество = 0
            if (!IndexInRange(index) || !Eq(Slots[index], value) || Counts[index] <= 0)
                return 0;
            
            return Counts[index];
        }

        public bool Remove(T value)
        {
            // возвращает true если value удалено
            // иначе false

            int index = SeekSlot(value);

            // если удаляемый на месте
            if (IndexInRange(index) && Counts[index] > 0 && Eq(Slots[index], value))
            {
                Counts[index]--;
                Sz--;
                if (Counts[index] == 0)
                    Counts[index] = -1;
                return true;
            }

            return false;
        }

        public Bag<T> Intersection(Bag<T> set2)
        {
            // пересечение текущего множества и set2
            Bag<T> ans = new();
            var data = GetActiveSlots();
            for (int i = 0; i < data.Values.Length; i++)
            {
                int count = Math.Min(data.Counts[i], set2.GetCountOf(data.Values[i]));
                for (int k = 0; k < count; k++)
                    ans.Put(data.Values[i]);
            }

            return ans;
        }

        public Bag<T> Union(Bag<T> set2)
        {
            // объединение текущего множества и set2
            Bag<T> ans = new();
            var data = GetActiveSlots();
            for (int i = 0; i < data.Values.Length; i++)
            {
                int count = Math.Max(data.Counts[i], set2.GetCountOf(data.Values[i]));
                for (int k = 0; k < count; k++)
                    ans.Put(data.Values[i]);
            }

            var data2 = set2.GetActiveSlots();
            for (int i = 0; i < data2.Values.Length; i++)
                if (GetCountOf(data2.Values[i]) == 0)
                    for (int k = 0; k < data2.Counts[i]; k++)
                        ans.Put(data2.Values[i]);

            return ans;
        }

        public Bag<T> Difference(Bag<T> set2)
        {
            // разница текущего множества и set2
            Bag<T> ans = new();
            var data = GetActiveSlots();
            for (int i = 0; i < data.Values.Length; i++)
            {
                int count = data.Counts[i] - set2.GetCountOf(data.Values[i]);
                for (int k = 0; k < count; k++)
                    ans.Put(data.Values[i]);
            }

            return ans;
            ;
        }

        public bool IsSubset(Bag<T> set2)
        {
            // возвращает true, если set2 есть
            // подмножество текущего множества,
            // иначе false
            var slots2 = set2.GetActiveSlots();
            for (int i = 0; i < slots2.Values.Length; i++)
                if (GetCountOf(slots2.Values[i]) < slots2.Counts[i])
                    return false;

            return true;
        }

        public bool Equals(Bag<T> set2)
        {
            // возвращает true, 
            // если set2 равно текущему множеству,
            // иначе false

            return IsSubset(set2) && set2.IsSubset(this);
        }

    }
}
