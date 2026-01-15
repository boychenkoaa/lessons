using System;
using System.Collections.Generic;

namespace AlgorithmsDataStructures
{

    public class Node
    {
        public int value;
        public Node next;
        public Node(int _value) { value = _value; }
    }

    public class LinkedList
    {
        public Node head;
        public Node tail;

        public LinkedList()
        {
            head = null;
            tail = null;
        }

        // команда, предусловий нет
        public void AddInTail(Node _item)
        {
            if (head == null) head = _item;
            else tail.next = _item;
            tail = _item;
        }

        // команда, предусловий нет
        public void AddInHead(Node _item)
        {
            if (IsEmpty()) tail = _item;
            else _item.next = head;
            head = _item;
        }

        public bool IsEmpty()
        {
            return head == null;
        }

        // запрос; предусловие -- элемент существует
        public Node Find(int _value)
        {
            Node node = head;
            while (node != null)
            {
                if (node.value == _value) return node;
                node = node.next;
            }
            return null;
        }

        //
        public List<Node> FindAll(int _value)
        {
            List<Node> nodes = new List<Node>();
            Node node = head;

            while (node != null)
            {
                if (node.value == _value)
                {
                    nodes.Add(node);
                }
                node = node.next;
            }

            return nodes;
        }

        public bool Remove(int _value)
        {
            // пустой
            if (IsEmpty())
            { return false; }

            // ровно 1 элемент и его нужно удалить
            if (head == tail && head.value == _value)
            {
                Clear();
                return true;
            }

            // > 1 элемента, удаляем голову
            if (head.value == _value)
            {
                head = head.next;
                return true;
            }

            // > 1 элемента, удаляем середину
            Node prev = head;
            Node node = head.next;

            while (node != null)
            {
                if (node.value == _value)
                {
                    // если удаляем хвост
                    if (node == tail) tail = prev;
                    prev.next = node.next;
                    return true;
                }
                node = node.next;
            }

            return false; // если узел был удалён
        }

        public void RemoveAll(int _value)
        {
            if (IsEmpty()) return;

            while (head.value == _value)
            {
                head = head.next;
            }
            Node prev = head;
            Node node = head.next;
            while (node != null)
            {
                if (node.value == _value)
                {
                    prev.next = node.next;
                }
                else
                {
                    prev = node;
                }
                node = node.next;
            }
        }

        public void Clear()
        {
            head = null;
            tail = null;
        }

        public int Count()
        {
            Node node = head;
            int ans = 0;
            while (node != null)
            {
                node = node.next;
                ans++;
            }
            return ans;
        }

        public void InsertAfter(Node _nodeAfter, Node _nodeToInsert)
        {
            // если пустой
            if (IsEmpty())
            {
                head = _nodeToInsert;
                tail = _nodeToInsert;
                return;

            }

            // вставка в начало непустого
            if (_nodeAfter == null)
            {
                _nodeToInsert.next = head;
                head = _nodeToInsert;
                return;
            }

            // в конец
            if (tail == _nodeAfter)
            {
                tail.next = _nodeToInsert;
                tail = _nodeToInsert;
                return;
            }

            // в середину
            _nodeToInsert.next = _nodeAfter.next;
            _nodeAfter.next = _nodeToInsert;
        }

        public void PrintValues()
        {
            Node node = head;
            while (node != null)
            {
                Console.Write(node.value);
                node = node.next;
            }

        }
    } // LinkedList


}
