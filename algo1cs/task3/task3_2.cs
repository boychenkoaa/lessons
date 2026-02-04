using System;
using System.Linq;
using Xunit;

namespace AlgorithmsDataStructures
{



    public class UnitTest1 : IDisposable
    {
        /*
        Тестируем реализацию, знаю что плохо
        куча констант...
        но тем не менее вставляю инварианты, где возможно

        тестируемые методы:
        MakeArray
        GetItem
        Append
        Insert
        Remove
        */
        public DynArray<int> dyn_arr = new DynArray<int>();
        public void Dispose() => AssertInvariants();

        protected void AssertInvariants()
        {
            Assert.True(dyn_arr.capacity <= 16 || dyn_arr.count * 2 >= dyn_arr.capacity); // инвариант -- процент заполнения не менее 0.5
        }

        [Fact]
        public void TestMakeArray()
        {
            Assert.Equal(16, dyn_arr.capacity);
            Assert.Equal(0, dyn_arr.count);
        }

        [Theory]
        [InlineData(new int[] { })]
        [InlineData(new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 })]
        public void TestAppend(int[] arr)
        {
            DynArray<int> dyn_arr = new DynArray<int>();
            foreach (int x in arr)
                dyn_arr.Append(x);

            Assert.True(arr.SequenceEqual(dyn_arr.array[0..dyn_arr.count]));

            Assert.Equal(arr.Length, dyn_arr.count);
        }

        public static TheoryData<int[], int> TheoryDataInsert()
        {
            var data = new TheoryData<int[], int>();
            data.Add(new int[] { 1, 2, 3 }, 0);
            data.Add(new int[] { 1, 2, 3 }, 1);
            data.Add(new int[] { 1, 2, 3 }, 2);
            data.Add(Enumerable.Range(1, 100).ToArray(), 0);
            data.Add(Enumerable.Range(1, 100).ToArray(), 1);
            data.Add(Enumerable.Range(1, 100).ToArray(), 99);
            data.Add(Enumerable.Range(1, 32).ToArray(), 0); // будет нужна реаллокация
            data.Add(Enumerable.Range(1, 32).ToArray(), 30); //  будет нужна реаллокация   
            return data;
        }

        [Theory]
        [MemberData(nameof(TheoryDataInsert))]
        public void TestInsertValid(int[] before, int index)
        {
            foreach (int x in before)
                dyn_arr.Append(x);
            int old_count = dyn_arr.count;
            int old_capacity = dyn_arr.capacity;
            dyn_arr.Insert(999, index);
            Assert.Equal(999, dyn_arr.GetItem(index));
            Assert.Equal(old_count, dyn_arr.count - 1);
            Assert.True(old_capacity == dyn_arr.capacity || old_capacity * 2 == dyn_arr.capacity);
        }


        public static TheoryData<int[], int> TheoryDataRemove()
        {
            var data = new TheoryData<int[], int>();
            data.Add(new int[] { 1, 2, 3 }, 0);
            data.Add(new int[] { 1, 2, 3 }, 1);
            data.Add(new int[] { 1, 2, 3 }, 2);
            data.Add(Enumerable.Range(1, 100).ToArray(), 0);
            data.Add(Enumerable.Range(1, 100).ToArray(), 1);
            data.Add(Enumerable.Range(1, 100).ToArray(), 50);
            data.Add(Enumerable.Range(1, 100).ToArray(), 99);
            data.Add(Enumerable.Range(1, 32).ToArray(), 0);
            data.Add(Enumerable.Range(1, 32).ToArray(), 16);
            data.Add(Enumerable.Range(1, 32).ToArray(), 31);
            return data;
        }

        [Theory]
        [MemberData(nameof(TheoryDataRemove))]
        public void TestRemoveValid(int[] before, int index)
        {
            foreach (int x in before)
                dyn_arr.Append(x);

            int value_for_remove = dyn_arr.GetItem(index);
            int old_count = dyn_arr.count;
            int old_capacity = dyn_arr.capacity;
            Assert.Contains(value_for_remove, dyn_arr.array[0..dyn_arr.count]);
            dyn_arr.Remove(index);
            Assert.DoesNotContain(value_for_remove, dyn_arr.array[0..dyn_arr.count]);
            Assert.Equal(old_count, dyn_arr.count + 1);
            Assert.True(old_capacity == dyn_arr.capacity);

            // удаляем больше половины элементов
            for (int i = 0; i <= old_count / 2; i++)
                dyn_arr.Remove(0);
            Assert.True(old_capacity > dyn_arr.capacity || old_capacity == 16);


        }
    }
}
