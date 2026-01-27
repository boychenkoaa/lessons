using System;
using System.Collections.Generic;

namespace AlgorithmsDataStructures
{

    public class NodeExt
    {
        public int value;
        public NodeExt next, prev;

        public NodeExt(int _value)
        {
            value = _value;
            next = null;
            prev = null;
        }
    }

    public class LinkedList3ext
    {
        public LinkedList3ext()
        {
            Dummy.next = Dummy;
            Dummy.prev = Dummy;
        }


        public NodeExt? Head
        {
            get { return IsEmpty ? null : Dummy.next; }
        }

        public NodeExt? Tail
        {
            get { return IsEmpty ? null : Dummy.next; }
        }

        // запрос -- пустой ли список
        // без предусловий
        public bool IsEmpty
        {
            get { return Dummy.next == Dummy; }
        }

        public NodeExt Dummy { get; } = new NodeExt(0);

        private void InsertAfter(NodeExt nodeAfter, int value)
        {
            NodeExt newNode = new NodeExt(value);
            newNode.next = nodeAfter.next;
            newNode.prev = nodeAfter.prev;
            nodeAfter.next.prev = newNode;
            nodeAfter.next = newNode;
        }


        public void InsertToHead(int value)
        {
            InsertAfter(Dummy, value);
        }

        public void InsertToTail(int value)
        {
            InsertAfter(Tail, value);
        }

        /*
        - Я понял задание как проверку списка на целостность (частный случай).
        - По крайней мере, у корректного списка никаких циклов внутри быть не может.
        - Кроме свойства next у ноды, мы не можем использовать буквально ничего (иначе проверка бессмысленна)
        - Для простоты используем встроенное множество,
        - А если бы было нельзя использовать стандартные структуры -- пришлось бы каждый раз иди по списку с начала
        и проверять, не было ли такой ноды у нас на пути. Это заняло бы квадратичное время в худшем случае.
        Ну, либо эти стандартные структуры реализовывать.
        */
        public bool HasCycles()
        {
            HashSet<NodeExt> visited = new HashSet<NodeExt> { };
            NodeExt node = Dummy.next;
            while ((node != Dummy) && (!visited.Contains(node)))
            {
                visited.Add(node);
                node = node.next;
            }
            return node != Dummy;

        }

        /*
        команда: инвертирование списка
        разворачиваем все элементы по отдельности
        */

        public void reverse()
        {
            // dummy меняем местами next <-> prev
            (Dummy.prev, Dummy.next) = (Dummy.prev, Dummy.next);
            NodeExt node = Dummy.prev; // бывший Next

            // аналогично поступаем для всех нод
            while (node != Dummy)
            {
                (node.prev, node.next) = (node.next, node.prev);
                node = node.prev;
            }
        }

        // сортировка
        public void BubbleSort()
        {
            if (IsEmpty)
                return;

            NodeExt node;
            NodeExt last = Tail;
            while (last != Head)
            {
                node = Head;
                while ((node != last) && (node.value > node.next.value))
                {
                    (node.value, node.next.value) = (node.next.value, node.value);
                    node = node.next;
                }
                last = last.prev;
            }
        }


        public void FromArray(int[] _list)
        {
            foreach (int _value in _list)
            {
                InsertToTail(_value);
            }
        }

        public int Count
        {
            get
            {
                NodeExt node = Head;
                int ans;
                for (ans = 0; node != null; ans++)
                    node = node.next;
                return ans;
            }
        }

        public int[] ToArray()
        {
            int[] ans = new int[Count];
            int i;
            NodeExt node = Head;
            for (i = 0; node != null; i++)
            {
                ans[i] = node.value;
                node = node.next;
            }
            return ans;
        }

        /*
        слияние списков
        сортируем списки, далее двигаем курсоры по обоим,
        добавляя меньший элемень в конец списка-результата
        далее дописываем остаток более длинного также в конец.
        */
        public LinkedList3ext Merge(LinkedList3ext other)
        {
            if (IsEmpty)
                return other;

            if (other.IsEmpty)
                return this;

            BubbleSort();
            other.BubbleSort();
            LinkedList3ext ans = new LinkedList3ext();
            NodeExt node = Head;
            NodeExt other_node = other.Head;

            // основа: двигаем курсор, у которого значение меньше,
            // добавляя это значение в итоговый список
            while ((node != Dummy) && (other_node != other.Dummy))
            {
                if (node.value < other_node.value)
                {
                    ans.InsertToTail(node.value);
                    node = node.next;
                }
                else
                {
                    ans.InsertToTail(other_node.value);
                    other_node = other_node.next;
                }
            }

            // добавляем "висячий" хвост
            NodeExt dummy;
            (node, dummy) = (node == Dummy) ? (other_node, other.Dummy) : (node, Dummy);
            while (node != dummy)
            {
                ans.InsertToTail(node.value);
                node = node.next;
            }
            return ans;
        }
    }
}
