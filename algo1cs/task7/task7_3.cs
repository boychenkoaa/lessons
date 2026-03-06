using System;
using System.Collections.Generic;

/*
рефлексия по задаче 5

5.3 (вращение по кругу)
Решено верно, но делал это вращение для очереди на двух стеках, там приходилось перемещать элементы между стеками.

5.4 (очередь на двух стеках)
Решено верно

5.5 (обращение через стек)
Решено верно, заполняем стек и опустошаем его

5.6 (циклическая очередь на базе массива фикс. размера)
Недоделано по невнимательности, банально почему-то забыл реализовать добавление. 
В следующем задании (деки) аналогичная задача реализована почти так же, как сказано в эталонном решении (head = (head + 1) % размер_массива).
За исключением того, что я не оставлял пустую ячейку, а явно хранил Size -- количество элементов в очереди.
*/

/*
Доп задания к заданию 7
Для простоты (и логарифмической сложности задачи на бин. поиск :) используем массив как внутреннее хранилище.
*/

namespace AlgorithmsDataStructures
{


    public class OrderedList3<T>
    {
        private List<T> _list = new();
        private bool _ascending;

        public T this[int index] => _list[index];
        public T[] ToArray() => _list.ToArray();

        public OrderedList3(bool asc)
        {
            _ascending = asc;
        }

        public int Compare(T v1, T v2)
        {
            int result = 0;
            string s1 = v1.ToString().Trim();
            string s2 = v2.ToString().Trim();
            result = s1.CompareTo(s2);

            return result;
            // -1 если v1 < v2
            // 0 если v1 == v2
            // +1 если v1 > v2
        }

        public bool IsEmpty => _list.Count == 0;

        // команда, вставка в пустой список
        // предусловие -- пуст
        public void AddToEmpty(T value)
        {
            if (!IsEmpty)
                throw new Exception("Ordered list is not empty");
            _list.Add(value);
        }

        // команда, вставка перед узлом
        private void AddBefore(Node<T> node, Node<T> node_before)
        {
            node.next = node_before;
            node.prev = node_before.prev;
            if (node.prev is not null)
                node.prev.next = node;
            node_before.prev = node;
        }

        // внутренние функции "сравнения", определяющие уже порядок в списке, с учетом _ascending
        // заодно прячем внуть выход за границы {-1; 0; 1} типа int
        private int CompareAsc(T v1, T v2) => _ascending ? Compare(v1, v2) : -(Compare(v1, v2));
        private bool Le(T v1, T v2) => CompareAsc(v1, v2) == -1;
        private bool Ge(T v1, T v2) => CompareAsc(v1, v2) == 1;
        private bool Eq(T v1, T v2) => CompareAsc(v1, v2) == 0;


        public void Add(T value)
        {
            // автоматическая вставка value 
            // в нужную позицию
            if (IsEmpty)
                AddToEmpty(value);

            // кс: если больше всех
            if (Ge(value, _list[^1]))
            {
                _list.Add(value);
                return;
            }
            // кс: если меньше всех
            if (Le(value, _list[0]))
            {
                _list.Insert(0, value);
                return;
            }

            // основная часть
            int index = _list.FindIndex(item => Ge(item, value));
            _list.Insert(index, value);
        }
        public void Delete(T val)
        {

            if (IsEmpty)
                return;

            int index = _list.FindIndex(item => Eq(item, val));
            if (index == -1)
                return;
            _list.RemoveAt(index);
        }

        public void Clear(bool asc)
        {
            _ascending = asc;
            _list.Clear();
        }

        public int Count()
        {
            return _list.Count;
        }

        /*
        задание 7.12
        запрос, найти узел с заданным значением
        предусловие -- не пуст
        ищет за O(log N) бинарным поиском
        возвращает индекс найденного элемента или -1, если элемент не найден
        */
        public int Find(T val)
        {
            if (IsEmpty)
                return -1;

            int left = 0;
            int right = _list.Count - 1;
            int mid = 0;
            // бинарный поиск классический
            while (left <= right)
            {
                mid = (left + right) / 2;
                if (Eq(_list[mid], val))
                    return mid;
                if (Le(_list[mid], val))
                    left = mid + 1;
                else
                    right = mid - 1;
            }
            return -1;
        }

        /*
        задание 7.8
        команда, удалить все дубликаты
        предусловие -- не пуст
        */

        public void RemoveDuplicates()
        {
            if (IsEmpty)
                return;
            List<T> new_list = new();
            new_list.Add(_list[0]);
            // проходим по всем элементам, кроме последнего
            for (int i = 0; i < _list.Count - 1; i++)
            {
                if (Eq(_list[i], _list[i + 1]))
                    continue;
                new_list.Add(_list[i]);
            }
            // отдельно обрабатываем последний
            if (!Eq(_list[^1], new_list[^1]))
                new_list.Add(_list[^1]);

            _list = new_list;
        }

        /*
            задание 7.9
            команда, объединить два упорядоченных списка
            предусловие -- одинаковый порядок. Пустые допускаются
            здесь используется обращение по индексу так как внутри массив, 
            по хорошему нужно делать итераторы, чтобы не зависеть от внутренней реализации
        */
        public OrderedList3<T> Merge(OrderedList3<T> other)
        {
            if (!_ascending != !other._ascending)
                throw new Exception("Ordered lists have different orders");

            OrderedList3<T> new_list = new(_ascending);
            int i = 0, j = 0;

            // проход по "общей" части списков
            // добавляем меньший элемент из двух текущих и двигаем индекс
            while (i < _list.Count && j < other._list.Count)
            {
                if (Le(_list[i], other._list[j]))
                    new_list.Add(_list[i++]);
                else
                    new_list.Add(other._list[j++]);
            }

            // проход по хвостам 
            // для одного из них цикл не выполнится ни разу -- он пуст, 
            // но мы не знаем, какой

            while (i < _list.Count)
                new_list.Add(_list[i++]);
            while (j < other._list.Count)
                new_list.Add(other._list[j++]);
            return new_list;
        }

        /*
        задание 7.10
        проверка на вхождение подсписка
        */

        public bool IsSubsequence(OrderedList3<T> other)
        {
            if (other.IsEmpty)
                return true;
            if (IsEmpty)
                return false;

            int i = 0, j = 0;
            // проход по "общей" части списков
            // если элемент совпал, то двигаем индекс подсписка
            while (i < _list.Count && j < other._list.Count)
            {
                if (Eq(_list[i], other._list[j]))
                    j++;
                i++;
            }
            // если индекс подсписка дошел до конца, то он является подсписком
            return j == other._list.Count;
        }

        /*
        задание 7.11
        найти наиболее часто встречающийся элемент
        предусловие -- не пуст
        */
        public T MostFrequent()
        {
            if (IsEmpty)
                throw new Exception("Ordered list is empty");
            T most_frequent = _list[0];
            int max_count = 1;
            int current_count = 1;
            // проходим по всем элементам, кроме последнего
            for (int i = 0; i < _list.Count - 1; i++)
            {
                if (Eq(_list[i], _list[i + 1]))
                    current_count++;
                else
                {
                    if (current_count > max_count)
                    {
                        max_count = current_count;
                        most_frequent = _list[i];
                    }
                    current_count = 1;
                }
            }
            // отдельно обрабатываем последний
            if (current_count > max_count)
                most_frequent = _list[^1];
            return most_frequent;
        }
    }
}