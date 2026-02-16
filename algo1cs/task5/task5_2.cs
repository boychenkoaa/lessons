using System;
using System.Linq;
using Xunit;

namespace AlgorithmsDataStructures
{
    public class QueueTest
    {
        [Theory]
        [InlineData(new int[] { })]
        [InlineData(new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 })]
        public void TestEnqDeq(int[] items)
        {
            Queue<int> q = new Queue<int>();
            foreach (int item in items)
            {
                int prev_len = q.Size();
                q.Enqueue(item);
                Assert.Equal(q.List.Last(), item);
                Assert.Equal(prev_len + 1, q.Size());
            }
            Assert.Equal(items.Length, q.Size());
            foreach (int item in items)
            {
                int prev_len = q.Size();
                int first = q.List.First();
                Assert.Equal(q.Dequeue(), first);
                Assert.Equal(item, first);
                Assert.Equal(prev_len - 1, q.Size());
            }
            Assert.Equal(0, q.Size());
        }
    }

}
