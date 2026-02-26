using System.Globalization;
using System.Reflection;
using AlgorithmsDataStructures;

namespace tests;

public class UnitTest1
{
    [Theory]
    [InlineData(new int[]{1,2,3,4,5})]
    public void TestAddFront(int [] arr)
    {
        // проверяем инварианты -- первый элемент равен данному, количество увеличилось на 1
        Deque<int> deque = new();
        foreach (int elem in arr)
        {
            int old_size = deque.Size();
            deque.AddFront(elem);
            Assert.Equal(deque.Size(), old_size + 1);
            Assert.Equal(deque.First(), elem);
        }
    }

    [Theory]
    [InlineData(new int[]{1,2,3,4,5})]
    public void TestAddTail(int [] arr)
    {
        // проверяем инварианты -- первый элемент равен данному, количество увеличилось на 1
        Deque<int> deque = new();
        foreach (int elem in arr)
        {
            int old_size = deque.Size();
            deque.AddTail(elem);
            Assert.Equal(deque.Size(), old_size + 1);
            Assert.Equal(deque.Last(), elem);
        }
    }

    [Theory]
    [InlineData(new int[]{1,2,3,4,5})]
    public void TestRemoveFront(int [] arr)
    {
        // проверяем инварианты -- первый элемент равен данному, количество увеличилось на 1
        Deque<int> deque = new();
        foreach (int elem in arr)
            deque.AddTail(elem);
    
        int N = arr.Length;
        Assert.Equal(N, deque.Size());

        for (int i = 0; i < N; i++)
        {
            Assert.Equal(deque.First(), arr[i]);
            int elem = deque.RemoveFront();
            Assert.Equal(elem, arr[i]);
            Assert.Equal(N-i-1, deque.Size());
        }
        Assert.True(deque.IsEmpty);
    }

        [Theory]
    [InlineData(new int[]{1,2,3,4,5})]
    public void TestRemoveTail(int [] arr)
    {
        // проверяем инварианты -- первый элемент равен данному, количество увеличилось на 1
        Deque<int> deque = new();
        foreach (int elem in arr)
            deque.AddTail(elem);
    
        int N = arr.Length;
        Assert.Equal(N, deque.Size());

        for (int i = N-1; i >= 0; i --)
        {
            Assert.Equal(deque.Last(), arr[i]);
            int elem = deque.RemoveTail();
            Assert.Equal(elem, arr[i]);
            Assert.Equal(i, deque.Size());
        }
        Assert.True(deque.IsEmpty);
    }

    [Fact]
    
    public void TestIsEmpty()
    {
        Deque<int> deque = new();
        Assert.True(deque.IsEmpty);
        deque.AddFront(1);
        Assert.False(deque.IsEmpty);
        deque.RemoveFront();
        Assert.True(deque.IsEmpty);
    }

}
