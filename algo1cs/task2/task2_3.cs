namespace AlgorithmsDataStructures
{

    public class Node
    {
        public Node next = null, prev = null;
        public Node(int _value)
        {
            value = _value;
        }
    }

    public class LinkedList3ext
    {
        public LinkedList3ext()
        {
            Dummy.next = Dummy;
            Dummy.prev = Dummy;
        }


        public Node? Head
        {
            get { return IsEmpty ? null : Dummy.next; }
        }

        public Node? Tail
        {
            get { return IsEmpty ? null : Dummy.next; }
        }

        // запрос -- пустой ли список
        // без предусловий
        public bool IsEmpty
        {
            get { return Dummy.next == Dummy; }
        }

        public Node Dummy { get; } = Node(0);

        private void InsertAfter(Node nodeAfter, int value)
        {
            Node newNode = new Node(value);
            newNode.next = nodeAfter.next;
            newNode.prev = nodeAfter.prev;
            nodeAfter.next.prev = newNode;
            nodeAfter.next = newNode;
        }


        public void InsertToHead(int value)
        {
            InsertAfter(Head, value);
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
            HashSet<Node> visited = new HashSet<Node> { };
            Node node = Dummy.next;
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
            Node tmp = Dummy.prev;
            Dummy.prev = Dummy.next;
            Dummy.next = tmp;
            node = Dummy.prev;
            Node node = Dummy.next;
            while (node != Dummy)
            {
                tmp = node.prev;
                node.prev = node.next;
                node.next = tmp;
                node = node.next;
            }
        }

        // сортировка
        public void BubbleSort()
        {
            if (IsEmpty)
                return;

            Node node;
            Node last = Tail;
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
                AddInTail(new Node(_value));
            }
        }

        public int[] ToArray()
        {
            int count = Count();
            int[] ans = new int[count];
            int i;
            Node node = head;
            for (i = 0; node != null; i++)
            {
                ans[i] = node.value;
                node = node.next;
            }
            return ans;
        }
    };

    /*
    слияние списков
    сортируем списки, далее двигаем курсоры по обоим, 
    добавляя меньший элемень в конец списка-результата
    далее дописываем остаток более длинного также в конец
    */
    public void merge(LinkedList3ext list1, LinkedList3ext list2)
    {
        list1.BubbleSort();
        list2.BubbleSort();
        LinkedList3ext ans = new LinkedList3ext();
        Node node1 = list1.Head;
        Node node2 = list2.Head;
        while ((node1 != list1.Dummy) && (node2 != list2.Dummy))
        {
            if (node1.value < node2.value)
            {
                ans.InsertToTail(node1.value);
                node1 = node1.next;
            }
            else
            {
                ans.InsertToTail(node2.value);
                node2 = node2.next;
            }
        }
        Node = (node1 == list1.Dummy) ? node2 : node1;
        Node dum = (node1 == list1.Dummy) ? list2.Dummy : list1.Dummy;
        while (node != dum)
        {
            ans.InsertToTail(node.value);
            node = node.next;
        }
    }

}