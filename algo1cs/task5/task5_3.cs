using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;

/*
рефлексия на задание 3

3.6 
формально решено верно, но -- неосознанно, наугад
добавлял в банк 2 элемента при добавлении и 1 при удалении, 
реаллокацию вверх и вниз оставил как у обычного массива -- потому что не придумал ничего другого, хотя и было краткое указание в задании
сейчас понял, что схема имеет вариации -- когда реаллокация, сколько списывать при реаллокации вниз

вывод 
1. надо быть осторожным с этими коэффициентами и не выходить за рамки теоретических оценок
2. коэффициенты на практике, если мы решили оптимизировать, скорее всего, "тюнингуются" под конкретную задачу

3.7 
все так (через одномерный массив), только реаллокация неудобная, статический массив проще :)
*/


namespace AlgorithmsDataStructures
{

    public class QueueSt2<T>
    {
        /*
        очередь на базе двух стеков
        основная идея -- добавляем в стек1, удаляем из стека 2
        если стек2 пуст -- копируем в него стек1 (как раз через push(pop) будет в нужном порядке, чтобы был FIFO)
        */
        Stack<T> stack1;
        Stack<T> stack2;

        public QueueSt2()
        {
            // инициализация внутреннего хранилища очереди
            stack1 = new Stack<T>();
            stack2 = new Stack<T>();
        }

        public void Enqueue(T item)
        {
            stack1.Push(item);
        }

        public T Dequeue()
        {
            if (IsEmpty)
                return default(T);

            if (stack2.Count > 0)
                return stack2.Pop();

            while (stack1.Count > 0)
            {
                stack2.Push(stack1.Pop());
            }

            return stack2.Pop();
        }

        public int Size()
        {
            return stack1.Count + stack2.Count; // размер очереди
        }

        private void shiftL()
        // <1234<  ==>  <2341<
        {
            // краевые случаи 
            if (IsEmpty)
                return;

            if (stack2.Count == 0)
                while (stack1.Count > 1)
                    stack2.Push(stack1.Pop());

            // типовой случай -- просто перекидываем из 2 в 1
            stack1.Push(stack2.Pop());
            return;
        }
        // зеркально shiftL
        private void shiftR()
        {
            // <1234<  ==>  <4123<
            // краевые случаи 
            if (IsEmpty)
                return;

            if (stack1.Count == 0)
            // перекидываем все кроме одного
            {
                while (stack2.Count > 1)
                    stack1.Push(stack2.Pop());

                return;
            }

            // типовой случай -- просто перекидываем из 1 в 2
            stack2.Push(stack1.Pop());

        }

        public bool IsEmpty => Size() == 0;

        public void ShiftRN(int N)
        {
            if (IsEmpty)
                return;
            int Nshifts = N % Size(); // если N велико, откидываем полные обороты по N раз -- берем только остаток от деления
            for (int i = 0; i < Nshifts; i++)
                for (int j = 0; j < N; j++)
                    shiftR();
        }

        public void ShiftLN(int N)
        {
            if (IsEmpty)
                return;
            int Nshifts = N % Size(); // если N велико, откидываем полные обороты
            for (int i = 0; i < Nshifts; i++)
                for (int j = 0; j < N; j++)
                    shiftL();
        }

        public void Reverse()
        {
            Stack<T> stack = new();
            while (!IsEmpty)
            {
                stack.Push(Dequeue());
            }

            while (stack.Count > 0)
            {
                Enqueue(stack.Pop());
            }
        }
    }

    public class QueueArr3<T>
    {
        /*
        очередь на базе массива
        при добавлении элемента -- сдвигаем левый указатель налево
        при удалении элемента -- сдвигаем правый указатель тоже налево
        если очередь пуста -- левый и правый равны 
        TODO доделать их сдвиг в конец при удалении
        если очередь заполнена -- левый указывает на конец массива, а правый на начало
        */

        T[] arr;
        int left; // указывает на первый свободный
        int right; // указывает на последний занятый

        public QueueArr3(int MaxCount)
        {
            // инициализация внутреннего хранилища очереди
            arr = new T[MaxCount];
            right = MaxCount - 1;
            left = MaxCount - 1;
        }

        private void reallocate()
        {
            int N = arr.Length;
            for (int i = 0; i < Size(); i++)
                arr[N - 1 - i] = arr[left - i];
            right = N - 1;
            left = N - Size() - 1;
        }
        public void Enqueue(T item)
        {
            if (IsFull)
                throw new Exception("Queue overflow");
            arr[left] = item;
            left -= 1;
        }

        public T Dequeue()
        {
            right -= 1;
            if (IsEmpty)
                right = left = arr.Length - 1;
            return arr[right];
        }

        public int Size()
        {
            return right - left; // размер очереди
        }
        public bool IsEmpty => Size() == 0;

        public bool IsFull => Size() == arr.Length;







    }

}



