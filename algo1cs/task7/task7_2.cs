using System.Collections.Generic;
using System.Data;

namespace AlgorithmsDataStructures
{

    public class UnitTest7
    {
        private static void AssertInvariants<T>(OrderedList<T> list, bool? ascending = null)
        {
            // целостность пустого списка
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
            int count = 0;
            Node<T> node = list.head;
            Node<T> prev = null;
            while (node != null)
            {
                Assert.Equal(prev, node.prev);
                if (prev != null && ascending.HasValue)
                {
                    int cmp = list.Compare(prev.value, node.value);
                    if (ascending.Value)
                        Assert.True(cmp <= 0);
                    else
                        Assert.True(cmp >= 0);
                }
                count++;
                prev = node;
                node = node.next;
            }
            Assert.Equal(list.tail, prev);
            Assert.Equal(count, list.Count());
        }

        private static OrderedList<int> OrderedListFromArray(int[] array, bool ascending)
        {
            OrderedList<int> list = new(ascending);
            foreach (int value in array)
            {
                list.Add(value);
            }
            return list;
        }

        /*
        всегда проверяем общий инвариант класса: отсортированность
        при добавлении / удалении длина списка должна увеличиться / уменьшиться на 1
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
        public void TestCompareNodesString(string val1, string val2, int result)
        {
            OrderedList<string> list = new(true);
            Assert.Equal(result, list.Compare(val1, val2));
        }

        [Theory]
        [InlineData(4, 5, -1)]
        [InlineData(5, 4, 1)]
        [InlineData(4, 4, 0)]
        public void TestCompareNodesInt(int val1, int val2, int result)
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
        [InlineData(true, new int[] { 42 }, new int[] { 42 })]
        [InlineData(true, new int[] { 42, 54 }, new int[] { 42, 54 })]
        [InlineData(true, new int[] { 54, 42, 36 }, new int[] { 36, 42, 54 })]
        [InlineData(true, new int[] { 3, 4, 2, 5, 1 }, new int[] { 1, 2, 3, 4, 5 })]
        [InlineData(false, new int[] { 42, 54 }, new int[] { 54, 42 })]
        [InlineData(false, new int[] { 54, 42, 36 }, new int[] { 54, 42, 36 })]
        [InlineData(false, new int[] { 3, 4, 2, 5, 1 }, new int[] { 5, 4, 3, 2, 1 })]
        public void TestAdd(bool ascending, int[] values, int[] result)
        {
            OrderedList<int> list = OrderedListFromArray(values, ascending);
            AssertInvariants(list, ascending);
            Assert.Equal(result.Length, list.Count());

            List<Node<int>> nodes = list.GetAll();
            int[] actual = nodes.ConvertAll(node => node.value).ToArray();
            Assert.Equal(result, actual);
        }

        [Theory]
        [InlineData(true, new int[] { 42 }, 42, new int[] { })]
        [InlineData(true, new int[] { 42, 54 }, 42, new int[] { 54 })]
        [InlineData(true, new int[] { 54, 42, 36 }, 42, new int[] { 36, 54 })]
        [InlineData(true, new int[] { 3, 4, 2, 5, 1 }, 4, new int[] { 1, 2, 3, 5 })]
        [InlineData(true, new int[] { 3, 4, 2, 5, 1 }, 5, new int[] { 1, 2, 3, 4 })]
        [InlineData(true, new int[] { 3, 4, 2, 5, 1 }, 1, new int[] { 2, 3, 4, 5 })]
        [InlineData(false, new int[] { 42 }, 42, new int[] { })]
        [InlineData(false, new int[] { 42, 54 }, 42, new int[] { 54 })]
        [InlineData(false, new int[] { 54, 42, 36 }, 42, new int[] { 54, 36 })]
        [InlineData(false, new int[] { 3, 4, 2, 5, 1 }, 4, new int[] { 5, 3, 2, 1 })]
        [InlineData(false, new int[] { 3, 4, 2, 5, 1 }, 5, new int[] { 4, 3, 2, 1 })]

        public void TestDelete(bool ascending, int[] values, int value, int[] result)
        {
            OrderedList<int> list = OrderedListFromArray(values, ascending);

            AssertInvariants(list, ascending);
            list.Delete(value);
            Assert.Equal(result.Length, list.Count());
            AssertInvariants(list, ascending);

            List<Node<int>> nodes = list.GetAll();
            int[] actual = nodes.ConvertAll(node => node.value).ToArray();
            Assert.Equal(result, actual);
        }

        [Theory]
        [InlineData(new int[] { 42, 54, 36 }, new int[] { 33, 41, 55, 101 })]
        public void TestFind(int[] values, int[] bad_values)
        {
            OrderedList<int> list = OrderedListFromArray(values, true);
            AssertInvariants(list, true);


            foreach (int v in values)
                Assert.Equal(v, list.Find(v).value);

            foreach (int bad_v in bad_values)
                Assert.Null(list.Find(bad_v));

            Assert.Null(list.Find(100));
        }
    }
}
