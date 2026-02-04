using System;
using System.Collections.Generic;

namespace AlgorithmsDataStructures
{

    public class DynArray<T>
    {
        public T[] array;
        public int count;
        public int capacity;

        public DynArray()
        {
            count = 0;
            MakeArray(16);
        }

        // команда -- реаллокация на объем new_capacity
        public void MakeArray(int new_capacity)
        {

            if (new_capacity < count)
            {
                throw new IndexOutOfRangeException();
            }
            
            T[] new_array = new T[new_capacity];
            
            for (int i = 0; i < count; i++)
            {
                new_array[i] = array[i];
            }
            array = new_array;
            capacity = new_capacity;

        }


        // возвращает index без изменений если он корректен, либо
        // бросает исключение при выходе за границы массива
        protected int get_safe_index(int index)
        {
            if ((index < 0) || (index >= count))
            {
                throw new IndexOutOfRangeException();
            }
            return index;

        }

        // запрос: является ли capacity недостаточным
        protected bool is_too_small()
        {
            return count == capacity;
        }

        // запрос: является ли capacity чрезмерным
        protected bool is_too_big()
        {
            return count < 0.5 * capacity;
        }

        // реаллокация вверх
        protected void reallocate_up()
        {
            MakeArray(capacity * 2);
        }

        // реаллокация вниз
        protected void reallocate_down()
        {
            int new_capacity = (int)(capacity * 2.0 / 3.0);
            new_capacity = (new_capacity < 16) ? 16 : new_capacity;
            MakeArray(new_capacity);
        }

        // команда -- реаллоцирует, если это необходимо,
        // проверяет оба условия (и если слишком мал, и если слишком велик)
        // после выполнения мы уверены, что места для будущей операции достаточно (и не слишком много)
        protected void check_count_and_reallocate()
        {
            if (is_too_big())
            {
                reallocate_down();
                return; // не забываем выйти, чтобы не случайно сработало второе условие
            }

            if (is_too_small())
            {
                reallocate_up();
            }
        }

        // запрос - взятие элемента по индексу
        public T GetItem(int index)
        {
            index = get_safe_index(index);
            return array[index];
        }

        // добавляет itm в конец
        public void Append(T itm)
        {
            check_count_and_reallocate();
            array[count] = itm;
            count++;
        }

        // добавление элемента на место index
        public void Insert(T itm, int index)
        {

            index = get_safe_index(index);
            check_count_and_reallocate();
            // сдвиг хвоста массива на 1 вправо
            for (int i = count; i > index; i--)
            {
                array[i] = array[i - 1];
            }
            array[index] = itm;
            count++;

        }

        // удаление элемента с индексом index
        public void Remove(int index)
        {
            index = get_safe_index(index);
            // сдвиг хвоста массива на 1 влево
            for (int i = index; i < count - 1; i++)
            {
                array[i] = array[i + 1];
            }
            count--;
            check_count_and_reallocate();
        }

    }
}
