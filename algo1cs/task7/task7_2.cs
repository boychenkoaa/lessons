
using System.Collections.Generic;
using System.Data;

namespace AlgorithmsDataStructures
{

    public class UnitTest7
    {
        /*
        всегда проверяем общий инвариант класса: отсортированность
        при добавлении / удалении длина списка должна увеличиться / уменьшиться на 1

        */
        [Theory]
        [InlineData("a", "b", -1)]
        [InlineData("b", "a", 1)]
        [InlineData("a", "a", 0)]
        [InlineData(" a ", "  b  ", -1)]
        [InlineData("  b  ", " a ", 1)]
        [InlineData("  a  ", " a ", 0)]

        public void TestCompareNodesString(string val1, string val2, int result)
        {
            OrderedList<string> list = new OrderedList<string>(true);
            Assert.Equal(result, list.Compare(val1, val2));
        }

        [Theory]
        [InlineData(4, 5, -1)]
        [InlineData(5, 4, 1)]
        [InlineData(4, 4, 0)]
        public void TestCompareNodesInt(int val1, int val2, int result)
        {
            OrderedList<int> list = new OrderedList<int>(true);
            Assert.Equal(result, list.Compare(val1, val2));
        }

        [Fact]
        public void TestIsEmpty()
        {
            OrderedList<int> list = new OrderedList<int>(true);
            Assert.True(list.IsEmpty);
            list.AddToEmpty(42);
            Assert.False(list.IsEmpty);
        }
        [Fact]
        public void TestCount()
        {
            OrderedList<int> list = new OrderedList<int>(true);
            Assert.Equal(0, list.Count());
            list.AddToEmpty(42);
            Assert.Equal(1, list.Count());
            list.Add(54);
            Assert.Equal(2, list.Count());
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
            OrderedList<int> list = new(ascending);
            foreach (int value in values)
            {
                list.Add(value);
            }
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
            OrderedList<int> list = new(ascending);
            foreach (int v in values)
            {
                list.Add(v);
            }
            list.Delete(value);
            Assert.Equal(result.Length, list.Count());

            List<Node<int>> nodes = list.GetAll();
            int[] actual = nodes.ConvertAll(node => node.value).ToArray();
            Assert.Equal(result, actual);
        }

        [Theory]
        [InlineData(new int[] { 42, 54, 36 }, new int[] { 33, 41, 55, 101 })]
        public void TestFind(int[] values, int[] bad_values)
        {
            OrderedList<int> list = new(true);
            foreach (int v in values)
                list.Add(v);


            foreach (int v in values)
                Assert.Equal(v, list.Find(v).value);

            foreach (int bad_v in bad_values)
                Assert.Null(list.Find(bad_v));

            Assert.Null(list.Find(100));
        }
    }


}