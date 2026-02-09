using System;
using System.Data;
using System.Linq;
using NuGet.Frameworks;
using Xunit;

namespace AlgorithmsDataStructures
{
    public class StackTest
    {
        [Theory]
        [InlineData(new int[]{}, null)]
        [InlineData(new int[]{1}, 1)]
        [InlineData(new int[]{1,2,3}, 3)]
        [InlineData(new int[]{1,2,3,4,5,6,7,8,9,10}, 10)]
        public void TestFromArrayPeek(int[] arr, int _peek)
        {
            Stack <int> stack = new();
            stack.FromArray(arr);
            Assert.Equal(stack.Peek(), _peek);
        }

        [Theory]
        [InlineData(new int[]{}, 0)]
        [InlineData(new int[]{1}, 1)]
        [InlineData(new int[]{1,2,3,4}, 4)]
        [InlineData(new int[]{1,2,3,4,5,6,7,8,9,10}, 10)]
        public void TestSize(int[] arr, int _size)
        {
            Stack <int> stack = new();
            stack.FromArray(arr);
            Assert.Equal(_size, stack.Size());
            for (int i = 0; i < _size; i++)
                stack.Push(i);
            Assert.Equal(2*_size, stack.Size());
            for (int i = 0; i < _size; i++)
                stack.Pop();
            Assert.Equal(_size, stack.Size());
        }

        [Theory]
        [InlineData(new int[]{}, default(int), new int[]{})]
        [InlineData(new int[]{1}, 1, new int[]{})]
        [InlineData(new int[]{1,2,3,4}, 4, new int[]{3,2,1})]
        [InlineData(new int[]{1,2,3,4,5,6,7,8,9,10}, 10, new int[]{9,8,7,6,5,4,3,2,1})]
        public void TestPop(int[] arr, int _peek, int[] arr_after )
        {
            Stack <int> stack = new();
            stack.FromArray(arr);
            int peek = stack.Pop();
            Assert.Equal(peek, _peek);
            Assert.Equal(stack.Size(), arr.Length > 0 ? arr.Length -1 : 0);
           
            Assert.True(arr_after.SequenceEqual(stack.ToArray));

        }

        [Theory]
        [InlineData(new int[]{}, 1, new int[]{1})]
        [InlineData(new int[]{1}, 2, new int[]{2, 1})]
        [InlineData(new int[]{1,2,3,4,5,6,7,8,9,10}, 11, new int[]{11,10,9,8,7,6,5,4,3,2,1})]
        public void testPush(int[] arr, int new_elem, int[] arr_after)
        {
            Stack <int> stack = new();
            stack.FromArray(arr);
            stack.Push(new_elem);
            Assert.Equal(stack.Size(), arr.Length+1);
            Assert.Equal(stack.Peek(), new_elem);
            Assert.True(arr_after.SequenceEqual(stack.ToArray));
        }

    }
}
