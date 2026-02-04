using System;
using System.Collections.Generic;
using System.Linq;

/*
рефлексия на задание 1.8* (суммирование списков)
- алгоритм верный,
- в случае неодинаковых длин возвращаю null
*/

namespace AlgorithmsDataStructures
{

    /*
    TODO динамический массив на основе банковского метода
    нужно добавить подсчет баланса
    общие соображения:
    - операция добавления в конец без реаллокации добавляет в банк 2 ед
    (одна оплачивает ее саму)
    - операция
    при реаллокации вверх баланс равен нулю?
    */

    // пока не сделано
    public class DynArrayBank<T>
    {
        public T[] array;
        public int count;
        public int capacity;

        public DynArrayBank()
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
            int old_capacity = capacity;
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
        protected int GetSafeIndex(int index)
        {
            if ((index < 0) || (index >= count))
            {
                throw new IndexOutOfRangeException();
            }
            return index;

        }

        protected bool IsTooSmall()
        {
            return count == capacity;
        }

        protected bool IsTooBig()
        {
            return count < 0.5 * capacity;
        }

        protected void ReallocateUp()
        {
            MakeArray(capacity * 2);
        }

        protected void ReallocateDown()
        {
            int new_capacity = (int)(capacity * 2.0 / 3.0);
            new_capacity = (new_capacity < 16) ? 16 : new_capacity;
            MakeArray(new_capacity);
        }

        // команда -- реаллоцирует, если это необходимо,
        // проверяет оба условия (и если слишком мал, и если слишком велик)
        // после выполнения мы уверены, что места для будущей операции достаточно (и не слишком много)
        protected void CheckCountAndReallocate()
        {
            if (IsTooBig())
            {
                ReallocateDown();
                return; // не забываем выйти, чтобы не случайно сработало второе условие
            }

            if (IsTooSmall())
            {
                ReallocateUp();
            }
        }

        // запрос - взятие элемента по индексу
        public T GetItem(int index)
        {
            index = GetSafeIndex(index);
            return array[index];
        }

        // добавляет itm в конец
        public void Append(T itm)
        {
            CheckCountAndReallocate();
            array[count] = itm;
            count++;
        }

        // добавление элемента на место index
        public void Insert(T itm, int index)
        {

            index = GetSafeIndex(index);
            CheckCountAndReallocate();
            // сдвиг хвоста массива на 1 вправо
            for (int i = count + 1; i > index; i--)
            {
                array[i] = array[i - 1];
            }
            array[index] = itm;
            count++;

        }

        // удаление элемента с индексом index
        public void Remove(int index)
        {
            index = GetSafeIndex(index);
            // сдвиг хвоста массива на 1 влево
            for (int i = index; i < count - 1; i++)
            {
                array[i] = array[i + 1];
            }
            count--;
            CheckCountAndReallocate();
        }

    }

    // статический массив
    // основная идея -- развернуть в одномерный массив
    // статически память выделяется
    public class MultiDimensionArray<T>
    {
        public T[] Arr;
        public int[] Dimensions;

        public int Count => Dimensions.Length != 0 ? Dimensions.Aggregate((acc, elem) => acc * elem) : 0;
        public int DimCount => Dimensions.Length;

        public MultiDimensionArray(params int[] _dimensions)
        {
            Dimensions = _dimensions;
            Arr = new T[Count];
        }

        // запрос -- "веса" размерностей
        public int[] Weigths
        /*
            пример:
            индексы                      0    1    2    3
            ---------------------------------------------
            размерности (dimensions):    2    4    6    8
            веса (weights):            192   48    8    1

            Вычисление весов:
            последний вес всегда = 1, далее в цикле справа налево
            weights[i] = weights[i+1] * dimensions[i+1]
        */

        {
            get
            {
                int[] ans = new int[Dimensions.Length];

                ans[^1] = 1;
                for (int i = Count-2; i >= 0; i--)
                    ans[i] = ans[i + 1] * Dimensions[i + 1];
                return ans;
            }
        }

        public int[] LinearToNd(int _index)
        {
            /*
            запрос: вычисление Nd-индекса по линейному
            Способ похож на переводом в систему счисления с переменным основанием, типа фибоначчиевой
            Пример. 
            Всего в примере выше 384 элемента
            Найдем мультииндекс для 380
            В начале R = 380
            Делим в цикле по i текущий остаток R на вес[i]
            380 / 192 = 1 остаток 188
            188 /  48 = 3 остаток 44
            44  /   8 = 5 остаток 4
            4   /   1 = 4 остаток 0
            Ответ: 1, 3, 5, 4
            Проверка: 1 х 192 + 3 х 48 + 5 х 8 + 4 х 1 = 192 + 144 + 40 + 4 = 192 + 188 = 380 
            */
            int[] ans = new int[DimCount];
            for (int i = 0; i < DimCount; i++)
            {
                ans[i] = _index / Weigths[i];
                _index %= Weigths[i];
            }
            return ans;
        }

        // многомерный => одномерный индекс
        // считается как скалярное произведение _NdIndex x Weights
        public int NdToLinear(int[] _NdIndex)
        {
            if (_NdIndex.Length != DimCount)
                throw new Exception("Incorrect _NdIndex length!");
            int [] w = Weigths;
            return w.Zip(_NdIndex, (w, i) => w * i).Sum();
        }


        // запрос -- попадает ли мульти-индекс в диапазон
        private bool IsMultiIndexInRange(int[] NdIndex)
        {
            // специально разбил на 2 части для простоты отладки
            bool isLengthsEqual = NdIndex.Length == Dimensions.Length;
            if (!isLengthsEqual)
                return false;

            // меньше поэлементно
            bool isAllElementsLess = NdIndex.Zip(Dimensions, (m, d) => m < d).All(x => x);
            return isAllElementsLess;
        }

        // безопасная обертка MultiIndexToLinear
        public int MultiIndexToLinearSafe(int[] multiIndex)
        {
            if (IsMultiIndexInRange(multiIndex))
                return NdToLinear(multiIndex);
            throw new IndexOutOfRangeException();
        }

        public T Get(params int[] multiIndex)
        {
            int index = MultiIndexToLinearSafe(multiIndex);
            return Arr[index];
        }

        public void Set(T new_value, params int[] multiIndex)
        {
            int index = MultiIndexToLinearSafe(multiIndex);
            Arr[index] = new_value;
        }

        /* 
        команда
        меняет размер ровно одного измерения
        копирует элементы при наличии Nd-индекса в обоих массивах
        цикл по 1d старым
        1d старый => Nd старый => Nd корректен в other? => 1d новый => присваивание
        
        TODO: оптимизировать (придумать формулу проверки, какие элементы выпадают / прибавляются при подобных реаллокациях, чтобы не проверять все в лоб)
        */
        public void Resize(int dimension, int new_size)
        {
            if ((dimension < 0) || (dimension >= DimCount))
                throw new IndexOutOfRangeException();
            if (new_size <= 0)
                throw new Exception("new_size is negative");


            // считаем новые веса и размерности, но пока что не замещаем ими старые
            int[] new_dimensions = new int[DimCount];
            for (int i = 0; i <DimCount; i++)
                new_dimensions[i] = Dimensions[i];
            new_dimensions[dimension] = new_size;
            
            MultiDimensionArray<T> other = new MultiDimensionArray<T>(new_dimensions);

            // копирование поэлементное other.Arr <- this.Arr через Nd-индексы (должны совпадать именно они, а не одномерные)
            for (int i = 0; i < Count; i++)
            {
                int[] nd_index = LinearToNd(i);
                if (other.IsMultiIndexInRange(nd_index))
                    other.Set(Arr[i], nd_index);
            }

            // поверхностная копия this <- other
            Dimensions = other.Dimensions;
            Arr = other.Arr;

        }

    }
}
