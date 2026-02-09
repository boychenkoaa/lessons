using System;
using System.Collections.Generic;
using System.Linq;

/*

Ответ на задание 3. 
Если размер стека -- четный, опустошит стек
Если нечетный, то последний Pop() будет вызван при пустом стеке
Будет выброшено исключение (либо сработает какая-либо еще обработка нештатных ситуаций на проекте)
*/

namespace AlgorithmsDataStructures
{

    public class Stack<T>
    {
        private LinkedList<T> list;
        private int _size;
        public Stack()
        {
            list = new LinkedList<T>();
            _size = 0;
        }

        public bool IsEmpty
        {
            get => _size == 0;
        }
        public int Size()
        {
            // размер текущего стека		  
            return _size;
        }

        public T Pop()
        {
            // ваш код
            if (IsEmpty)
                return default(T);

            T peek = Peek();
            list.RemoveFirst();
            _size --;
            return peek; // null, если стек пустой
        }

        public void Push(T val)
        {
            list.AddFirst(val);
            _size++;
        }

        public T Peek()
        {
            // ваш код
            if (IsEmpty)
                return default(T);
            return list.First.Value;
        }

        public T[] ToArray => list.ToArray<T>();

        public void FromArray(T[] arr)
        {
            foreach (T t in arr)
                Push(t);
        }
    }

}