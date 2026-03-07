using System;
using System.Collections.Generic;
using System.Runtime.Intrinsics.Arm;

namespace AlgorithmsDataStructures
{

    public class Node<T>
    {
        public T value;
        public Node<T> next, prev;

        public Node(T _value)
        {
            value = _value;
            next = null;
            prev = null;
        }

    }

    public class OrderedList<T>
    {
        public Node<T> head, tail;
        private bool _ascending;

        public OrderedList(bool asc)
        {
            head = null;
            tail = null;
            _ascending = asc;
        }

        public int Compare(T v1, T v2)
        {
            int result = 0;
            if(typeof(T) == typeof(String))
            {
                String s1 = v1.ToString().Trim();
                String s2 = v2.ToString().Trim();
                result = s1.CompareTo(s2);
            }
            else 
            {
                result = Comparer<T>.Default.Compare(v1, v2);
                // универсальное сравнение
            }
            if (result > 0)
                result = 1;
            if (result < 0)
                result = -1;
            
            return result;
            // -1 если v1 < v2
            // 0 если v1 == v2
            // +1 если v1 > v2
        }

        public bool IsEmpty => head is null;

        // команда, вставка в пустой список
        // предусловие -- пуст
        public void AddToEmpty(T value)
        {
            if (!IsEmpty)
                throw new Exception("Ordered list is not empty");
            head = new Node<T>(value);
            tail = head;
        }

        // команда, вставка перед узлом
        private static void AddBefore(Node<T> node, Node<T> node_before)
        {
            node.next = node_before;
            node.prev = node_before.prev;
            if (node.prev is not null)
                node.prev.next = node;
            node_before.prev = node;
        }

        // внутренние функции "сравнения", определяющие уже порядок в списке, с учетом _ascending
        // заодно прячем внуть выход за границы {-1; 0; 1} типа int
        private int CompareNodes(Node<T> node1, Node<T> node2) => _ascending ? Compare(node1.value, node2.value) : -(Compare(node1.value, node2.value));
        private bool Le(Node<T> node1, Node<T> node2) => CompareNodes(node1, node2) == -1;
        private bool Ge(Node<T> node1, Node<T> node2) => CompareNodes(node1, node2) == 1;
        private bool Eq(Node<T> node1, Node<T> node2) => CompareNodes(node1, node2) == 0;
        private bool EqVal(Node<T> node, T value) => Compare(node.value, value) == 0;

        public void Add(T value)
        {
            // автоматическая вставка value 
            // в нужную позицию
            if (IsEmpty)
            {
                AddToEmpty(value);
                return;
            }

            Node<T> new_node = new(value);

            // кс: если больше всех
            if (Ge(new_node, tail))
            {
                tail.next = new_node;
                new_node.prev = tail;
                tail = new_node;
                return;
            }
            // кс: если меньше всех
            if (Le(new_node, head))
            {
                AddBefore(new_node, head);
                head = new_node;
                return;
            }

            // основная часть
            Node<T> node = head;
            while (node != null && Le(node, new_node))
                node = node.next;
            AddBefore(new_node, node);
        }

        private static void DeleteNode(Node<T> node)
        {
            if (node.prev is not null)
                node.prev.next = node.next;

            if (node.next is not null)
                node.next.prev = node.prev;
        }

        public void Delete(T val)
        {

            if (IsEmpty)
                return;

            // ищем ноду для удаления
            Node<T> node = head, tmp_node = new(val);
            while (node != null && Le(node, tmp_node))
                node = node.next;

            // кс: если не нашли
            if (node is null || !EqVal(node, val))
                return;

            // кс: удаление единственного элемента
            if (head == tail)
            {
                Clear(_ascending);
                return;
            }

            // кс: удаление головы
            if (node == head)
            {
                head = node.next;
                DeleteNode(node);
                return;
            }

            // кс: удаление хвоста
            if (node == tail)
            {
                tail = node.prev;
                DeleteNode(node);
                return;
            }

            // удаление середины
            DeleteNode(node);
        }

        public void Clear(bool asc)
        {
            _ascending = asc;
            head = null;
            tail = null;
        }

        public int Count()
        {
            int count = 0;
            Node<T> node = head;
            while (node != null)
            {
                count++;
                node = node.next;
            }
            return count;
        }

        public Node<T> Find(T val)
        {
            if (IsEmpty)
                return null;

            Node<T> node = head, tmp_node = new(val);
            while (node != null && Le(node, tmp_node))
            {
                node = node?.next;
            }
            if (node == null) // дошли до конца и не нашли
            {
                return null;
            }

            if (!EqVal(node, val)) // не дошли до конца, и не нашли
                return null;

            return node;
        }

        public List<Node<T>> GetAll() // выдать все элементы упорядоченного 
                                      // списка в виде стандартного списка
        {
            List<Node<T>> r = new();
            Node<T> node = head;
            while (node != null)
            {
                r.Add(node);
                node = node.next;
            }
            return r;
        }


    }
}
