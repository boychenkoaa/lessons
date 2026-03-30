using System;
using Xunit;

namespace AlgorithmsDataStructures
{
    public class UnitTest10_2
    {
        // генерирует множетсва типа {"a1", "a2", "a3", ... "a_count"} с заданным количеством элементов и префиксом
        private static string[] GenerateValues(int count, string prefix)
        {
            string[] values = new string[count];
            for (int i = 0; i < count; i++)
                values[i] = prefix + i;
            return values;
        }

        private static PowerSet<string> BuildSet(string[] values)
        {
            PowerSet<string> set = new PowerSet<string>();
            foreach (string value in values)
                set.Put(value);
            return set;
        }

        private static void AssertSetEqual(PowerSet<string> set, string[] values)
        {
            string[] actual = set.GetActiveSlots();
            Assert.Equal(values.Length, actual.Length);
            foreach (string value in values)
                Assert.Contains(value, actual);
        }

        [Theory]
        [InlineData(new string[0], new string[0], 0)]
        [InlineData(new[] { "a", "b" }, new string[0], 2)]
        [InlineData(new[] { "a", "a", "b" }, new string[0], 2)]
        [InlineData(new[] { "a", "b", "c" }, new[] { "b" }, 2)]
        [InlineData(new[] { "a" }, new[] { "x" }, 1)]
        public void testSize(string[] arr, string[] arrToRemove, int ans)
        {
            PowerSet<string> set = BuildSet(arr);
            foreach (string value in arrToRemove)
                set.Remove(value);
            Assert.Equal(ans, set.Size());
        }

        [Theory]
        [InlineData(new string[0], "a", 1)]
        [InlineData(new[] { "a" }, "a", 1)]
        [InlineData(new[] { "a", "b" }, "c", 3)]
        [InlineData(new[] { "a", "b" }, "a", 2)]
        public void testPut(string[] values, string value, int newSize)
        {
            PowerSet<string> set = BuildSet(values);
            set.Put(value);
            Assert.Equal(newSize, set.Size());
            Assert.True(set.Get(value));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, "a", true)]
        [InlineData(new[] { "a", "b" }, "c", false)]
        [InlineData(new string[0], "a", false)]
        public void testGet(string[] values, string value, bool ans)
        {
            PowerSet<string> set = BuildSet(values);
            Assert.Equal(ans, set.Get(value));
            set.Remove(value);
            Assert.False(set.Get(value));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, "a", true, 1, false)]
        [InlineData(new[] { "a", "b" }, "c", false, 2, false)]
        [InlineData(new[] { "a", "b", "c" }, "b", true, 2, false)]
        [InlineData(new string[0], "a", false, 0, false)]
        public void testRemove(string[] values, string value, bool ans, int size, bool hasValue)
        {
            PowerSet<string> set = BuildSet(values);
            bool removed = set.Remove(value);
            Assert.Equal(ans, removed);
            Assert.Equal(size, set.Size());
            Assert.Equal(hasValue, set.Get(value));
        }

        [Theory]
        [InlineData(new string[0], new string[0], new string[0])]
        [InlineData(new[] { "a", "b" }, new string[0], new[] { "a", "b" })]
        [InlineData(new[] { "a", "b", "c" }, new[] { "b" }, new[] { "a", "c" })]
        [InlineData(new[] { "a", "a" }, new string[0], new[] { "a" })]
        [InlineData(new[] { "a", "b", "c" }, new[] { "a", "c" }, new[] { "b" })]
        public void testGetActiveSlots(string[] values, string[] valuesToRemove, string[] ans)
        {
            PowerSet<string> set = BuildSet(values);
            foreach (string value in valuesToRemove)
                set.Remove(value);
            AssertSetEqual(set, ans);
        }

        [Theory]
        [InlineData(-1, false)]
        [InlineData(0, true)]
        [InlineData(19999, true)]
        [InlineData(20000, false)]
        public void testIndexInRange(int index, bool ans)
        {
            PowerSet<string> set = new PowerSet<string>();
            Assert.Equal(ans, set.IndexInRange(index));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "c" }, new[] { "b" })]
        [InlineData(new[] { "a" }, new[] { "b" }, new string[0])]
        [InlineData(new[] { "a", "b" }, new[] { "a", "b" }, new[] { "a", "b" })]
        [InlineData(new string[0], new[] { "a" }, new string[0])]
        [InlineData(new[] { "a", "b" }, new[] { "b" }, new[] { "b" })]
        public void testIntersection(string[] arr1, string[] arr2, string[] ans)
        {
            PowerSet<string> set1 = BuildSet(arr1);
            PowerSet<string> set2 = BuildSet(arr2);
            PowerSet<string> result = set1.Intersection(set2);
            AssertSetEqual(result, ans);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "c" }, new[] { "a", "b", "c" })]
        [InlineData(new[] { "a" }, new string[0], new[] { "a" })]
        [InlineData(new string[0], new[] { "b" }, new[] { "b" })]
        [InlineData(new string[0], new string[0], new string[0])]
        [InlineData(new[] { "a", "b" }, new[] { "a" }, new[] { "a", "b" })]
        public void testUnion(string[] arr1, string[] arr2, string[] ans)
        {
            PowerSet<string> set1 = BuildSet(arr1);
            PowerSet<string> set2 = BuildSet(arr2);
            PowerSet<string> result = set1.Union(set2);
            AssertSetEqual(result, ans);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "c" }, new[] { "a" })]
        [InlineData(new[] { "a" }, new[] { "a" }, new string[0])]
        [InlineData(new[] { "a", "b" }, new string[0], new[] { "a", "b" })]
        [InlineData(new string[0], new[] { "a" }, new string[0])]
        [InlineData(new[] { "a", "b" }, new[] { "a", "b" }, new string[0])]
        public void testDifference(string[] arr1, string[] arr2, string[] ans)
        {
            PowerSet<string> set1 = BuildSet(arr1);
            PowerSet<string> set2 = BuildSet(arr2);
            PowerSet<string> result = set1.Difference(set2);
            AssertSetEqual(result, ans);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "a" }, true)]
        [InlineData(new[] { "a", "b" }, new[] { "c" }, false)]
        [InlineData(new[] { "a", "b" }, new string[0], true)]
        [InlineData(new[] { "a" }, new[] { "a", "b" }, false)]
        [InlineData(new string[0], new string[0], true)]
        public void testIsSubset(string[] set_a, string[] subset_of_a, bool ans)
        {
            PowerSet<string> set = BuildSet(set_a);
            PowerSet<string> subset = BuildSet(subset_of_a);
            Assert.Equal(ans, set.IsSubset(subset));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "a" }, true)]
        [InlineData(new[] { "a", "b" }, new[] { "a" }, false)]
        [InlineData(new string[0], new string[0], true)]
        [InlineData(new string[0], new[] { "a" }, false)]
        [InlineData(new[] { "a" }, new[] { "a", "b" }, false)]
        public void testEquals(string[] set_a, string[] set_b, bool ans)
        {
            PowerSet<string> set1 = BuildSet(set_a);
            PowerSet<string> set2 = BuildSet(set_b);
            Assert.Equal(ans, set1.Equals(set2));
        }

        /*
        нагрузочные тесты с большими множествами
        */
        [Fact]
        public void testPutGetLarge()
        {
            /*
            заполняем до отказа, проверяем что все на месте
            */
            string[] values = GenerateValues(20000, "v");
            PowerSet<string> set = BuildSet(values);
            Assert.Equal(20000, set.Size());
            Assert.True(set.Get("v0"));
            Assert.True(set.Get("v19999"));
        }

        [Fact]
        public void testReuseSlots()
        {
            /*
             проверяем работу с коллизиями 
             хеш-функция может и хороша, но при таком заполнении коллизии обязательно будут
             проверяем также корректное выставление статусов -- удаляем и добавляем 5000 элементов
            */
            string[] values = GenerateValues(20000, "v");
            PowerSet<string> set = BuildSet(values);
            
            for (int i = 0; i < 5000; i++)
                Assert.True(set.Remove("v" + i));
            Assert.Equal(15000, set.Size());
            for (int i = 0; i < 5000; i++)
                set.Put("n" + i);
            Assert.Equal(20000, set.Size());
            Assert.True(set.Get("n0"));
            Assert.True(set.Get("n4999"));
        }

        [Fact]
        public void testGetActiveSlotsLarge()
        {
            /*
            проверка корректного выставления статуса активного элемента
            */
            string[] values = GenerateValues(20000, "v");
            PowerSet<string> set = BuildSet(values);
            for (int i = 0; i < 1000; i++)
                set.Remove("v" + i);
            string[] active = set.GetActiveSlots();
            Assert.Equal(19000, active.Length);
            Assert.Contains("v1000", active);
            Assert.Contains("v19999", active);
        }

        [Fact]
        public void testIntersectionLarge()
        {
            /*
            проверка пересечения больших множеств
            */
            string[] a = GenerateValues(20000, "v");
            string[] b = GenerateValues(10000, "v");
            PowerSet<string> set1 = BuildSet(a);
            PowerSet<string> set2 = BuildSet(b);
            PowerSet<string> result = set1.Intersection(set2);
            Assert.Equal(10000, result.Size());
            Assert.True(result.Get("v0"));
            Assert.False(result.Get("v15000"));
        }

        [Fact]
        public void testUnionLarge()
        {
            /*
            проверка объединения больших множеств
            */
            string[] a = GenerateValues(10000, "v");
            string[] b = GenerateValues(10000, "w");
            PowerSet<string> set1 = BuildSet(a);
            PowerSet<string> set2 = BuildSet(b);
            PowerSet<string> result = set1.Union(set2);
            Assert.Equal(20000, result.Size());
            Assert.True(result.Get("v0"));
            Assert.True(result.Get("w9999"));
        }

        [Fact]
        public void testDifferenceLarge()
        {
            /*
            проверка разности больших множеств
            */
            string[] a = GenerateValues(20000, "v");
            string[] b = GenerateValues(15000, "v");
            PowerSet<string> set1 = BuildSet(a);
            PowerSet<string> set2 = BuildSet(b);
            PowerSet<string> result = set1.Difference(set2);
            Assert.Equal(5000, result.Size());
            Assert.False(result.Get("v0"));
            Assert.True(result.Get("v19999"));
        }

        [Fact]
        public void testIsSubsetLarge()
        {
            /*
            проверка вхождения для больших множеств
            */
            string[] a = GenerateValues(20000, "v");
            string[] b = GenerateValues(10000, "v");
            PowerSet<string> set1 = BuildSet(a);
            PowerSet<string> set2 = BuildSet(b);
            Assert.True(set1.IsSubset(set2));
            Assert.False(set2.IsSubset(set1));
        }

        [Fact]
        public void testEqualsLarge()
        {
            /*
            проверка равенства для больших множеств
            */
            string[] a = GenerateValues(20000, "v");
            string[] b = GenerateValues(20000, "v");
            PowerSet<string> set1 = BuildSet(a);
            PowerSet<string> set2 = BuildSet(b);
            Assert.True(set1.Equals(set2));
        }
    }
}
