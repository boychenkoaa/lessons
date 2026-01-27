namespace AlgorithmsDataStructures
{

    public class Node
    {
        public int value;
        public Node next, prev;

        public Node(int _value)
        {
            value = _value;
            next = null;
            prev = null;
        }
    }

    public class LinkedList2
    {
        public Node head;
        public Node tail;

        public LinkedList2()
        {
            head = null;
            tail = null;
        }

        // запрос -- пустой ли список
        // без предусловий
        public bool IsEmpty()
        {
            return head == null;
        }

        // добавление в пустой список
        // предусловие -- список пуст
        public void AddToEmpty(Node _item)
        {
            head = _item;
            tail = _item;
            head.next = null;
            head.prev = null;
        }

        // добавление в конец списка
        // без предусловий (хотя по хорошему сделать бы чтобы был непустой)
        public void AddInTail(Node _item)
        {
            if (IsEmpty())
            {
                AddToEmpty(_item);
            }
            else
            {
                tail.next = _item;
                _item.prev = tail;
            }
            tail = _item;
        }

        // добавление элемента в голову списка
        public void AddInHead(Node _item)
        {
            if (IsEmpty())
            {
                AddToEmpty(_item);
                return;
            }

            _item.next = head;
            head.prev = _item;
            _item.prev = null;
            head = _item;
        }

        // запрос на поиск ноды списка с первым вхождением _value
        public Node Find(int _value)
        {
            // здесь будет ваш код поиска
            Node node = head;
            while ((node != null) && (node.value != _value))
            {
                node = node.next;
            }

            return node;
        }

        // запрос на поиск всех вхождений
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

        // команда
        // удаляет первое вхождение значения _value
        // возвращает false если значения нет
        // и true если нашел и удалил
        public bool Remove(int _value)
        {
            Node node = Find(_value);

            if (node == null)
            {
                return false;
            }

            // краевые случаи
            if (node == head)
            {
                RemoveFromHead();
                return true;
            }

            if (node == tail)
            {
                RemoveFromTail();
                return true;
            }

            // основной случай
            RemoveNode(node);
            return true;
        }

        // команда: удаление из головы (ничего не делает, если пуст)
        public void RemoveFromHead()
        {
            if (IsEmpty())
                return;
            if (head == tail)
            {   
                Clear();
                return;
            }
            head = head?.next;
            head?.prev = null;
        }

        // команда: удаление из хвоста (ничего не делает, если пуст)
        public void RemoveFromTail()
        {
            if (IsEmpty())
                return;
            if (head == tail)
            {   
                Clear();
                return;
            }
            
            tail = tail.prev;
            tail.next = null;
        }

        // команда: удаление ноды
        public static void RemoveNode(Node _node)
        {
            _node.next?.prev = _node.prev;
            _node.prev?.next = _node.next;
        }


        public void RemoveAll(int _value)
        {
            // здесь будет ваш код удаления всех узлов по заданному значению
            // удаляем всех с головы
            while (head?.value == _value)
            {
                RemoveFromHead();
            }
            // удаляем всех с хвоста
            while (tail?.value == _value)
            {
                RemoveFromTail();
            }
            // удаляем всех из середины
            Node node = head;
            while (node != null)
            {
                if (node.value == _value)
                {
                    RemoveNode(node);
                }
                node = node.next;
            }
        }

        // очистка
        public void Clear()
        {
            head = null;
            tail = null;
        }
        // запрос -- количество элементов
        public int Count()
        {
            Node node = head;
            int ans;
            // тут использовал for, сообразил, немного непривычно
            for (ans = 0; node != null; ans++)
            {
                node = node.next;
            }
            return ans; // здесь будет ваш код подсчёта количества элементов в списке
        }


        // команда -- вставка ноды после заданной
        public void InsertAfter(Node _nodeAfter, Node _nodeToInsert)
        {
            // здесь будет ваш код вставки узла после заданного узла

            // если _nodeAfter = null
            // добавьте новый элемент первым в списке
            if (_nodeAfter == null)
            {
                AddInHead(_nodeToInsert);
                return;
            }

            if (_nodeAfter == tail)
            {
                AddInTail(_nodeToInsert);
                return;
            }

            _nodeToInsert.next = _nodeAfter.next;
            _nodeToInsert.prev = _nodeAfter;
            _nodeAfter.next.prev = _nodeToInsert;
            _nodeAfter.next = _nodeToInsert;
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
    }
}
