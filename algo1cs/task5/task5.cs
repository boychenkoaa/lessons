using System;
using System.Collections.Generic;
using System.Linq;

namespace AlgorithmsDataStructures
{

    public class Queue<T>
    {
        LinkedList<T> list = new();

        public LinkedList<T> List => list;
        public Queue()
        {
            // инициализация внутреннего хранилища очереди
        }

        public void Enqueue(T item)
        {
            // вставка в хвост
            list.AddLast(item);
        }

        public T Dequeue()
        {
            if (list.Count > 0)
            {
                T head = list.First();
                list.RemoveFirst();
                return head;
            }
            return default(T);

        }

        public int Size()
        {
            return list.Count; // размер очереди
        }

        public bool IsEmpty => list.Count == 0;

        /*
        можно было бы взять за основу свой список и перебросить ссылки у его N-го элемента, а не у каждого
        но сложность останется той же -- нужно все равно дойти до Nго элемента
        */
    }
}