using System;
using Xunit;

namespace AlgorithmsDataStructures
{
    public class UnitTest10_4
    {
        public static TheoryData<string[], int[], (string, int)[]> CartesianProductContentsData => new()
        {
            { new[] { "a", "b" }, 
            new[] { 1, 2 }, 
            new (string, int)[] { ("a", 1), ("a", 2), ("b", 1), ("b", 2) } 
            },
            { new[] { "a" }, 
            new[] { 1, 2 }, 
            new (string, int)[] { ("a", 1), ("a", 2) } }
        };

        private static PowerSet<T> BuildSet<T>(T[] values)
        {
            PowerSet<T> set = new PowerSet<T>();
            foreach (T value in values)
                set.Put(value);
            return set;
        }

        private static Bag<string> BuildBag(string[] values)
        {
            Bag<string> bag = new Bag<string>();
            foreach (string value in values)
                bag.Put(value);
            return bag;
        }

        private static void AssertSetEqual<T>(PowerSet<T> set, T[] expected)
        {
            T[] actual = set.GetActiveSlots();
            Assert.Equal(expected.Length, actual.Length);
            foreach (T value in expected)
                Assert.Contains(value, actual);
        }

        private static void AssertBagEqual(Bag<string> bag, string[] expectedValues, int[] expectedCounts)
        {
            var data = bag.GetActiveSlots();
            Assert.Equal(data.Values.Length, data.Counts.Length);
            Assert.Equal(expectedValues.Length, expectedCounts.Length);
            Assert.Equal(expectedValues.Length, data.Values.Length);
            string[] actualValues = data.Values;
            int[] actualCounts = data.Counts;
            string[] expectedValuesCopy = (string[])expectedValues.Clone();
            int[] expectedCountsCopy = (int[])expectedCounts.Clone();
            Array.Sort(actualValues, actualCounts);
            Array.Sort(expectedValuesCopy, expectedCountsCopy);
            Assert.Equal(expectedValuesCopy, actualValues);
            Assert.Equal(expectedCountsCopy, actualCounts);
        }

        [Theory]
        [InlineData(new string[0], new string[0], 0)]
        [InlineData(new[] { "a", "b", "a" }, new string[0], 3)]
        [InlineData(new[] { "a", "b", "a" }, new[] { "a" }, 2)]
        [InlineData(new[] { "a", "b", "a" }, new[] { "a", "a", "b" }, 0)]
        [InlineData(new[] { "a" }, new[] { "x" }, 1)]
        public void testSize(string[] values, string[] valuesToRemove, int ans)
        {
            Bag<string> bag = BuildBag(values);
            foreach (string value in valuesToRemove)
                bag.Remove(value);
            Assert.Equal(ans, bag.Size());
        }

        [Theory]
        [InlineData(new string[0], "a", 1)]
        [InlineData(new[] { "a" }, "a", 2)]
        [InlineData(new[] { "a", "b" }, "c", 3)]
        [InlineData(new[] { "a", "b", "a" }, "a", 4)]
        public void testPut(string[] values, string value, int newSize)
        {
            Bag<string> bag = BuildBag(values);
            bag.Put(value);
            Assert.Equal(newSize, bag.Size());
            Assert.True(bag.Has(value));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, "a", true)]
        [InlineData(new[] { "a", "b" }, "c", false)]
        [InlineData(new[] { "a", "a" }, "a", true)]
        [InlineData(new string[0], "a", false)]
        public void testGet(string[] values, string value, bool ans)
        {
            Bag<string> bag = BuildBag(values);
            int countBefore = bag.GetCountOf(value);
            Assert.Equal(ans, countBefore > 0);
            bag.Remove(value);
            int countAfter = bag.GetCountOf(value);
            if (countBefore > 0)
                Assert.Equal(countBefore - 1, countAfter);
            else
                Assert.Equal(0, countAfter);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, "a", true, new[] { "b" }, new[] { 1 })]
        [InlineData(new[] { "a", "b" }, "c", false, new[] { "a", "b" }, new[] { 1, 1 })]
        [InlineData(new[] { "a", "b", "c" }, "b", true, new[] { "a", "c" }, new[] { 1, 1 })]
        [InlineData(new[] { "a", "a" }, "a", true, new[] { "a" }, new[] { 1 })]
        [InlineData(new[] { "a", "a", "b" }, "a", true, new[] { "a", "b" }, new[] { 1, 1 })]
        [InlineData(new[] { "a"}, "a", true, new string[0], new int[0])]
        [InlineData(new[] { "a", "b", "b" }, "b", true, new[] { "a", "b" }, new[] { 1, 1 })]
        public void testRemove(string[] values, string valueToRemove, bool ans, string[] ansValues, int[] ansCounts)
        {
            Bag<string> bag = BuildBag(values);
            bool removeResult = bag.Remove(valueToRemove);
            Assert.Equal(ans, removeResult);
            AssertBagEqual(bag, ansValues, ansCounts);
        }

        [Theory]
        [InlineData(new string[0], new string[0], new string[0], new int[0])]
        [InlineData(new[] { "a", "b" }, new string[0], new[] { "a", "b" }, new[] { 1, 1 })]
        [InlineData(new[] { "a", "b", "c" }, new[] { "b" }, new[] { "a", "c" }, new[] { 1, 1 })]
        [InlineData(new[] { "a", "a" }, new string[0], new[] { "a" }, new[] { 2 })]
        [InlineData(new[] { "a", "b", "c" }, new[] { "a", "c" }, new[] { "b" }, new[] { 1 })]
        public void testGetActiveSlots(string[] values, string[] valuesToRemove, string[] ansValues, int[] ansCounts)
        {
            Bag<string> bag = BuildBag(values);
            foreach (string value in valuesToRemove)
                bag.Remove(value);
            AssertBagEqual(bag, ansValues, ansCounts);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "c" }, new[] { "b" }, new[] { 1 })]
        [InlineData(new[] { "a" }, new[] { "b" }, new string[0], new int[0])]
        [InlineData(new[] { "a", "b" }, new[] { "a", "b" }, new[] { "a", "b" }, new[] { 1, 1 })]
        [InlineData(new string[0], new[] { "a" }, new string[0], new int[0])]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a" }, new[] { "a" }, new[] { 1 })]
        public void testIntersection(string[] arr1, string[] arr2, string[] ansValues, int[] ansCounts)
        {
            Bag<string> bag1 = BuildBag(arr1);
            Bag<string> bag2 = BuildBag(arr2);
            Bag<string> result = bag1.Intersection(bag2);
            AssertBagEqual(result, ansValues, ansCounts);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "c" }, new[] { "a", "b", "c" }, new[] { 1, 1, 1 })]
        [InlineData(new[] { "a" }, new string[0], new[] { "a" }, new[] { 1 })]
        [InlineData(new string[0], new[] { "b" }, new[] { "b" }, new[] { 1 })]
        [InlineData(new string[0], new string[0], new string[0], new int[0])]
        [InlineData(new[] { "a", "a" }, new[] { "a", "b" }, new[] { "a", "b" }, new[] { 2, 1 })]
        public void testUnion(string[] arr1, string[] arr2, string[] ansValues, int[] ansCounts)
        {
            Bag<string> bag1 = BuildBag(arr1);
            Bag<string> bag2 = BuildBag(arr2);
            Bag<string> result = bag1.Union(bag2);
            AssertBagEqual(result, ansValues, ansCounts);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "c" }, new[] { "a" }, new[] { 1 })]
        [InlineData(new[] { "a" }, new[] { "a" }, new string[0], new int[0])]
        [InlineData(new[] { "a", "b" }, new string[0], new[] { "a", "b" }, new[] { 1, 1 })]
        [InlineData(new string[0], new[] { "a" }, new string[0], new int[0])]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a" }, new[] { "a", "b" }, new[] { 1, 1 })]
        public void testDifference(string[] arr1, string[] arr2, string[] ansValues, int[] ansCounts)
        {
            Bag<string> bag1 = BuildBag(arr1);
            Bag<string> bag2 = BuildBag(arr2);
            Bag<string> result = bag1.Difference(bag2);
            AssertBagEqual(result, ansValues, ansCounts);
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "a" }, true)]
        [InlineData(new[] { "a", "b" }, new[] { "c" }, false)]
        [InlineData(new[] { "a", "b" }, new string[0], true)]
        [InlineData(new[] { "a" }, new[] { "a", "a" }, false)]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a", "b" }, true)]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a", "a", "b" }, true)]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a", "a", "a" }, false)]
        [InlineData(new string[0], new string[0], true)]
        public void testIsSubset(string[] set_a, string[] subset_of_a, bool ans)
        {
            Bag<string> bag = BuildBag(set_a);
            Bag<string> subset = BuildBag(subset_of_a);
            Assert.Equal(ans, bag.IsSubset(subset));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { "b", "a" }, true)]
        [InlineData(new[] { "a", "b" }, new[] { "a" }, false)]
        [InlineData(new string[0], new string[0], true)]
        [InlineData(new string[0], new[] { "a" }, false)]
        [InlineData(new[] { "a" }, new[] { "a", "a" }, false)]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a", "a", "b" }, true)]
        [InlineData(new[] { "a", "a", "b" }, new[] { "a", "b" }, false)]
        public void testEquals(string[] set_a, string[] set_b, bool ans)
        {
            Bag<string> bag1 = BuildBag(set_a);
            Bag<string> bag2 = BuildBag(set_b);
            Assert.Equal(ans, bag1.Equals(bag2));
        }

        [Theory]
        [InlineData(new[] { "a", "b" }, new[] { 1, 2 }, 4)]
        [InlineData(new string[0], new[] { 1 }, 0)]
        public void testCartesianProductSize(string[] left, int[] right, int expectedSize)
        {
            PowerSet<string> set1 = BuildSet(left);
            PowerSet<int> set2 = BuildSet(right);
            PowerSet<(string, int)> result = PowerSet3<string>.CartesianProduct(set1, set2);
            Assert.Equal(expectedSize, result.Size());
        }

        [Theory]
        [MemberData(nameof(CartesianProductContentsData))]
        public void testCartesianProductContents(string[] left, int[] right, (string, int)[] expected)
        {
            PowerSet<string> set1 = BuildSet(left);
            PowerSet<int> set2 = BuildSet(right);
            PowerSet<(string, int)> result = PowerSet3<string>.CartesianProduct(set1, set2);
            AssertSetEqual(result, expected);
        }

        [Theory]
        [InlineData(new[] { "a", "b", "c" }, new[] { "b", "c", "d" }, new[] { "c", "b" }, new[] { "b", "c" })]
        [InlineData(new[] { "a" }, new[] { "b" }, new[] { "a", "b" }, new string[0])]
        public void testMultiIntersection(string[] s1, string[] s2, string[] s3, string[] expected)
        {
            PowerSet<string>[] sets = new[]
            {
                BuildSet(s1),
                BuildSet(s2),
                BuildSet(s3)
            };
            PowerSet<string> result = PowerSet3<string>.MultiIntersection(sets);
            AssertSetEqual(result, expected);
        }
    }
}
