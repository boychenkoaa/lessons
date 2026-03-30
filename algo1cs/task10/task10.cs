using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;


namespace AlgorithmsDataStructures
{

    public class PowerSet<T>
    {
        private enum SlotState : byte
        {
            Empty = 0,
            Active = 1,
            Deleted = 2
        }

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
        private SlotState[] States = new SlotState[Capacity];
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

            while (States[index] != SlotState.Empty &&
                   !(States[index] == SlotState.Active && Eq(Slots[index], value)))
            {
                // обновляем firstDeletedIndex
                if (States[index] == SlotState.Deleted && firstDeletedIndex == -1)
                    firstDeletedIndex = index;

                // основной шаг
                index = (index + 1) % Slots.Length;

                // если вернулись в начало -- все заполнено
                if (index == start_index)
                    return firstDeletedIndex;
            }


            if (States[index] == SlotState.Active) // нашли value
                return index;
            // если "мертвых" слотов не было -- вернем первый пустой, иначе первый "мертвый"
            return firstDeletedIndex == -1 ? index : firstDeletedIndex;
        }

        public PowerSet()
        {
            // ваша реализация хранилища
            Sz = 0;
        }

        public int Size()
        {
            // количество элементов в множестве
            return Sz;
        }

        public T[] GetActiveSlots()
        {
            T[] ans = new T[Sz];
            int j = 0;
            for (int i = 0; i < Slots.Length; i++)
            {
                if (States[i] == SlotState.Active)
                {
                    ans[j] = Slots[i];
                    j++;
                }
            }
            return ans;
        }

        public bool IndexInRange(int index) => index > -1 && index < Slots.Length;
        public void Put(T value)
        {
            /*
            команда: положить элемент во множество
            */
            int index = SeekSlot(value);
            if (!IndexInRange(index) || States[index] == SlotState.Active)
                return;

            Slots[index] = value;
            States[index] = SlotState.Active;
            Sz++;
        }

        public bool Get(T value)
        {
            // возвращает true если value имеется в множестве,
            // иначе false
            int index = SeekSlot(value);
            bool ans = IndexInRange(index) && States[index] == SlotState.Active && Eq(Slots[index], value);
            return ans;
        }

        public bool Remove(T value)
        {
            // возвращает true если value удалено
            // иначе false

            int index = SeekSlot(value);

            // если удаляемый на месте
            if (IndexInRange(index) && States[index] == SlotState.Active && Eq(Slots[index], value))
            {
                States[index] = SlotState.Deleted;
                Sz--;
                return true;
            }

            return false;
        }

        public PowerSet<T> Intersection(PowerSet<T> set2)
        {
            // пересечение текущего множества и set2
            PowerSet<T> ans = new();
            foreach (T slot in GetActiveSlots())
                if (set2.Get(slot))
                    ans.Put(slot);

            return ans;
        }

        public PowerSet<T> Union(PowerSet<T> set2)
        {
            // объединение текущего множества и set2
            PowerSet<T> ans = new();
            foreach (T slot in GetActiveSlots())
                ans.Put(slot);

            foreach (T slot2 in set2.GetActiveSlots())
                ans.Put(slot2);

            return ans;
        }

        public PowerSet<T> Difference(PowerSet<T> set2)
        {
            // разница текущего множества и set2
            PowerSet<T> ans = new();
            foreach (T slot in GetActiveSlots())
                if (!set2.Get(slot))
                    ans.Put(slot);

            return ans;
            ;
        }

        public bool IsSubset(PowerSet<T> set2)
        {
            // возвращает true, если set2 есть
            // подмножество текущего множества,
            // иначе false
            foreach (T slot2 in set2.GetActiveSlots())
                if (!Get(slot2))
                    return false;

            return true;
        }

        public bool Equals(PowerSet<T> set2)
        {
            // возвращает true, 
            // если set2 равно текущему множеству,
            // иначе false

            return IsSubset(set2) && set2.IsSubset(this);
        }

    }
}
