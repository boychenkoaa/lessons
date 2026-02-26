using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Runtime.CompilerServices;

/* 
_____ Рефлексия на задание 4 _____
Все задания решены неоптипально

4.4 и 4.5 
Без словаря, на ветвлениях

4.6 
Стек минимумов вел синхронно с основным -- и добавление, и удаление. Неоправданный перерасход по памяти.

4.7 
Держал стек средних арифметических (когда в руках молоток -- все становится гвоздями :). Перерасход. Но в пользу своего решения могу сказать, что переполнения не будет, в отличие от суммы. 

4.8 
Копипастил вычисление каждой операции, конечно же :\
*/

/*
___К задачам 6*___
- для простоты в доп задачах дек будет из int-ов
- все задачи в одном классе

6.4 
- метод is_palindrom

6.5 
- метод Min 
- поле MinArr + его синхронизация с Arr везде
- основная идея -- хранить и реаллоцировать массив минимумов вместе с основным. 
- тогда минимум на весь массив будет всегда или первым или последним.

6.6 (весь класс)
- основная идея -- хранить индекс первого элемента (L) и размер массива (Size)
- при добавлении и удалении слева надо циклически сдвигать индекс влево на 1 и менять Size
- при добавлении и удалении справа просто менять Size
*/
namespace AlgorithmsDataStructures
{

    class DequeArr
    {
        private int [] Arr;
        private int [] MinArr;
        private int L;
        public int Size = 0;
        private int Capacity => Arr.Length;

        private bool IsEmpty => Size == 0;


        public DequeArr()
        {
            // инициализация внутреннего хранилища
            Arr = new int[16];
            MinArr = new int[16];
            L = 7;
            Size = 0;

        }

        private int IncIndex(int index)
        {
            return (index + 1) % Capacity;
        }

        private int DecIndex(int index)
        {
            return (index - 1 + Capacity) % Capacity;
        }

        private static int Min2(int a, int b)
        {
            return a < b ? a : b;
        }

        private static int Min3(int a, int b, int c)
        {
            return Min2(Min2(a, b), c);
        }

        private int R => (L + Size - 1) % Capacity;
        
        private void Realloc(int new_capacity)
        {
            int[] new_array = new int[new_capacity];
            int[] new_min_array = new int[new_capacity];
            int j = L;
            for (int i = 0; i < Size; i++)
            {
                new_array[i] = Arr[j];
                new_min_array[i] = MinArr[j];
                j = IncIndex(j);
            }
            L = 0;
            Arr = new_array;
            MinArr = new_min_array;

        }

        private void check_and_realloc()
        {
            // если полностью заполнен
            if (Size == Capacity)
            {
                Realloc(Capacity * 2);
                return;
            }
            // если слишком мало
            if (Size <= Capacity / 2)
            {
                int new_capacity = Capacity / 3 * 2;
                if (new_capacity < 16)
                    new_capacity = 16;
                Realloc(new_capacity);
                return;
            }
        }


        public void AddFront(int item)
        {
            // добавление в голову
            check_and_realloc();
            int min = Min3(item, Arr[L], Arr[R]);
            L = DecIndex(L);
            Arr[L] = item;
            MinArr[L] = min;
            Size++;
        }

        public void AddTail(int item)
        {
            // добавление в хвост
            // L не трогаем
            check_and_realloc();
            int min = Min3(item, Arr[L], Arr[R]);
            int R1 = IncIndex(R) ;
            Arr[R1] = item;
            MinArr[R1] = min;
            Size++;
        }

        public void RemoveFront()
        {
            // удаление из головы
            L = IncIndex(L);
            Size--;
        }

        public void RemoveTail()
        {
            // удаление из хвоста
            Size--;
        }

        // 6.5* -- минимум за O(1)
        public int Min()
        {
            if (IsEmpty)
                throw new Exception("Min: deque is empty");
            return Min2(Arr[L], Arr[R]);
        }

        // 6.4* -- проверка на палиндром
        public static bool is_palindrom(string s)
        {
            Deque<char> deque = new();
            foreach (char c in s)
                deque.AddTail(c);

            int N = s.Length;
            for (int i = 0; i < N / 2; i++)
            {
                if (deque.First() != deque.Last())
                {
                    return false;
                }
                deque.RemoveFront();
                deque.RemoveTail();
            }

            return true;
        }
    }
    

}