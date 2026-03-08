namespace AlgorithmsDataStructures
{

    public class UnitTest7
    {
        private static void AssertInvariants<T>(OrderedList<T> list, bool ascending)
        {
            // проверка для пустого списка
            if (list.IsEmpty)
            {
                Assert.Null(list.head);
                Assert.Null(list.tail);
                Assert.Equal(0, list.Count());
                return;
            }

            // целостность непустого списка
            Assert.NotNull(list.head);
            Assert.NotNull(list.tail);
            Assert.Null(list.head.prev);
            Assert.Null(list.tail.next);

            // проверка на отсортированность, целостность, количество элементов
            int count = 1;
            Node<T> node = list.head.next;
            Node<T> prev = list.head;
            while (node != null)
            {
                Assert.Equal(prev, node.prev);
                int cmp_result = list.Compare(prev.value, node.value);
                Assert.True(ascending && cmp_result <= 0 || !ascending && cmp_result >= 0);
                count++;
                prev = node;
                node = node.next;
            }

            Assert.Equal(count, list.Count());
        }

        private bool CompareWithAns(OrderedList<int> list, int[] ans_asc, bool ascending)
        {

            if (list.Count() != ans_asc.Length)
                return false;
            if (!ascending)
                ans_asc = ans_asc.Reverse().ToArray();
            Node<int> node = list.head;
            foreach (int elem in ans_asc)
            {
                if (node == null || node.value != elem)
                    return false;
                node = node.next;
            }
            return true;
        }

        private static OrderedList<int> OrderedListFromArray(int[] array, bool ascending)
        {
            OrderedList<int> list = new(ascending);
            foreach (int value in array)
                list.Add(value);
            return list;
        }

        /*
        проверка добавления в пустой список
        */
        [Fact]
        public void TestAdd_EmptyList()
        {
            OrderedList<int> list = new(true);
            list.Add(42);
            Assert.Equal(1, list.Count());
            Assert.Equal(42, list.head.value);
            Assert.Equal(42, list.tail.value);
            Assert.True(list.head == list.tail);
            AssertInvariants(list, true);
        }


        [Theory]
        [InlineData("a", "b", -1)]
        [InlineData("b", "a", 1)]
        [InlineData("a", "a", 0)]
        [InlineData(" a ", "  b  ", -1)]
        [InlineData("  b  ", " a ", 1)]
        [InlineData("  a  ", " a ", 0)]
        public void TestCompareValuesString(string val1, string val2, int result)
        {
            OrderedList<string> list = new(true);
            Assert.Equal(result, list.Compare(val1, val2));
        }

        [Theory]
        [InlineData(4, 5, -1)]
        [InlineData(5, 4, 1)]
        [InlineData(4, 4, 0)]
        public void TestCompareValuesInt(int val1, int val2, int result)
        {
            OrderedList<int> list = new(true);
            Assert.Equal(result, list.Compare(val1, val2));
        }

        [Fact]
        public void TestIsEmpty()
        {
            OrderedList<int> list = new(true);
            Assert.True(list.IsEmpty);
            list.AddToEmpty(42);
            Assert.False(list.IsEmpty);
            AssertInvariants(list, true);
        }
        [Fact]
        public void TestCount()
        {
            OrderedList<int> list = new(true);
            Assert.Equal(0, list.Count());
            list.AddToEmpty(42);
            Assert.Equal(1, list.Count());
            list.Add(54);
            Assert.Equal(2, list.Count());
            AssertInvariants(list, true);
        }

        [Theory]
        [InlineData(new int[] { 1 }, new int[] { 1 })]
        [InlineData(new int[] { 1, 2 }, new int[] { 1, 2 })]
        [InlineData(new int[] { 2, 1 }, new int[] { 2, 1 })]
        [InlineData(new int[] { 1, 2, 3 }, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 1, 3, 2 }, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 2, 1, 3 }, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 2, 3, 1 }, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 3, 1, 2 }, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 3, 2, 1 }, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 1, 1, 2, 3 }, new int[] { 1, 1, 2, 3 })]
        [InlineData(new int[] { 1, 1, 3, 2 }, new int[] { 1, 1, 2, 3 })]
        [InlineData(new int[] { 2, 1, 1, 3 }, new int[] { 1, 1, 2, 3 })]
        [InlineData(new int[] { 3, 1, 1, 2 }, new int[] { 1, 1, 2, 3 })]
        [InlineData(new int[] { 3, 2, 1, 1 }, new int[] { 1, 1, 2, 3 })]
        [InlineData(new int[] { 2, 3, 1, 1 }, new int[] { 1, 2, 2, 3 })]
        [InlineData(new int[] { 1, 1, 2, 2 }, new int[] { 1, 1, 2, 2 })]
        [InlineData(new int[] { 2, 2, 1, 1 }, new int[] { 1, 1, 2, 2 })]
        [InlineData(new int[] { 1, 2, 1, 2 }, new int[] { 1, 1, 2, 2 })]
        [InlineData(new int[] { 2, 1, 2, 1 }, new int[] { 1, 1, 2, 2 })]
        [InlineData(new int[] { 3, 4, 2, 5, 1 }, new int[] { 1, 2, 3, 4, 5 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5 }, new int[] { 1, 2, 3, 4, 5 })]
        [InlineData(new int[] { 5, 4, 3, 2, 1 }, new int[] { 1, 2, 3, 4, 5 })]
        [InlineData(new int[] { 3, 3, 4, 4, 2, 2, 5, 5, 1, 1 }, new int[] { 1, 1, 2, 2, 3, 3, 4, 4, 5, 5 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5, 1, 2, 3, 4, 5 }, new int[] { 1, 1, 2, 2, 3, 3, 4, 4, 5, 5 })]
        [InlineData(new int[] { 1, 1, 2, 2, 3, 3, 4, 4, 5, 5 }, new int[] { 1, 1, 2, 2, 3, 3, 4, 4, 5, 5 })]
        [InlineData(new int[] { 5, 5, 4, 4, 3, 3, 2, 2, 1, 1 }, new int[] { 1, 1, 2, 2, 3, 3, 4, 4, 5, 5 })]
        public void TestAdd(int[] values, int[] ans)
        {
            // для true
            OrderedList<int> list = OrderedListFromArray(values, true);
            AssertInvariants(list, true);
            CompareWithAns(list, ans, true);

            // для false
            list = OrderedListFromArray(values, false);
            AssertInvariants(list, false);
            CompareWithAns(list, ans, false);
        }

        [Theory]
        [InlineData(new int[] { 1 }, 1, new int[] { })]
        [InlineData(new int[] { 1, 2 }, 1, new int[] { 2 })]
        [InlineData(new int[] { 1, 2 }, 2, new int[] { 1 })]
        [InlineData(new int[] { 1, 2, 3, 4 }, 1, new int[] { 2, 3, 4 })]
        [InlineData(new int[] { 1, 2, 3, 4 }, 2, new int[] { 1, 3, 4 })]
        [InlineData(new int[] { 1, 2, 3, 4 }, 3, new int[] { 1, 2, 4 })]
        [InlineData(new int[] { 1, 2, 3, 4 }, 4, new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 1, 1, 2, 2, 3, 3, 4, 4 }, 1, new int[] { 1, 2, 2, 3, 3, 4, 4 })]
        [InlineData(new int[] { 1, 1, 2, 2, 3, 3, 4, 4 }, 2, new int[] { 1, 1, 2, 3, 3, 4, 4 })]
        [InlineData(new int[] { 1, 1, 2, 2, 3, 3, 4, 4 }, 3, new int[] { 1, 1, 2, 2, 3, 4, 4 })]
        [InlineData(new int[] { 1, 1, 2, 2, 3, 3, 4, 4 }, 4, new int[] { 1, 1, 2, 2, 3, 3, 4 })]

        public void TestDelete(int[] values, int value, int[] ans)
        {
            // для true
            OrderedList<int> list = OrderedListFromArray(values, true);
            AssertInvariants(list, true);
            list.Delete(value);
            AssertInvariants(list, true);
            CompareWithAns(list, ans, true);

            // для false
            list = OrderedListFromArray(values, false);
            AssertInvariants(list, false);
            list.Delete(value);
            AssertInvariants(list, false);
            CompareWithAns(list, ans, false);
        }


        [Theory]
        [InlineData(new int[] { 42, 54, 36 }, new int[] { 33, 41, 55, 101 })]
        public void TestFind(int[] values, int[] bad_values)
        {
            // для true
            OrderedList<int> list = OrderedListFromArray(values, true);
            AssertInvariants(list, true);

            foreach (int v in values)
                Assert.Equal(v, list.Find(v).value);

            foreach (int bad_v in bad_values)
                Assert.Null(list.Find(bad_v));

            // для false
            list = OrderedListFromArray(values, false);
            AssertInvariants(list, false);

            foreach (int v in values)
                Assert.Equal(v, list.Find(v).value);

            foreach (int bad_v in bad_values)
                Assert.Null(list.Find(bad_v));

        }
    }
}
