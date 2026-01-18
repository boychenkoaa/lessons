namespace AlgorithmsDataStructures
{
    /*
        место для рефлексии
        (видимо, в следующем уроке будут эталонные решения)
    */
    public class LinkedListExt
    {
        public static LinkedList? SumValues(LinkedList list1, LinkedList list2)
        {
            if (list1.Count() != list2.Count())
            {
                return null;
            }

            LinkedList ans = new LinkedList();
            Node node1 = list1.head;
            Node node2 = list2.head;
            while (node1 != null)
            {
                ans.AddInTail(new Node(node1.value + node2.value));
                node1 = node1.next;
                node2 = node2.next;
            }

            return ans;
        }
    }
}