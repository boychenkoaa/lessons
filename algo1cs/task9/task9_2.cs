namespace AlgorithmsDataStructures
{

    public class UnitTest9
    {
        private static NativeDictionary<string> DictFromValues(int size, string[] keys)
        {
            NativeDictionary<string> dict = new(size);
            foreach (string key in keys)
                dict.Put(key, $"v-{key}");
            return dict;
        }

        private static bool CheckInvariants<T>(NativeDictionary<T> dict)
        {
            if (dict.size != dict.slots.Length) return false;
            if (dict.size != dict.values.Length) return false;

            for (int i = 0; i < dict.size; i++)
            {
                if (dict.slots[i] is null)
                    continue;
                if (!Equals(dict.values[i], dict.Get(dict.slots[i])))
                    return false;
            }

            return true;
        }

        [Theory]
        [InlineData("", 17, 0)]
        [InlineData("a", 17, 7)]
        [InlineData("az", 17, 15)]
        [InlineData("a", 5, 4)]
        [InlineData("az", 5, 4)]
        public void TestHashFun(string key, int size, int expectedIndex)
        {
            NativeDictionary<int> dict = new(size);
            Assert.Equal(expectedIndex, dict.HashFun(key));
        }

        [Theory]
        [InlineData(new string[] { "a", "b", "c" }, new string[] { "a", "b", "c" })]
        [InlineData(new string[] { "", "a", "b" }, new string[] { "", "a", "b" })]
        [InlineData(new string[] { "a", "a", "a" }, new string[] { "a" })]
        public void TestPut(string[] inputKeys, string[] expectedKeys)
        {
            NativeDictionary<string> dict = new(2*inputKeys.Length+1);
            foreach (string key in inputKeys)
                dict.Put(key, $"v-{key}");

            foreach (string key in expectedKeys)
                Assert.Equal($"v-{key}", dict.Get(key));

            Assert.True(CheckInvariants(dict));
        }

        [Theory]
        [InlineData(new string[] { "a", "b", "c" }, "b", "v-b")]
        [InlineData(new string[] { "a", "b", "c" }, "x", null)]
        [InlineData(new string[] { "" }, "", "v-")]
        public void TestGet(string[] keys, string key, string expected)
        {
            NativeDictionary<string> dict = DictFromValues(5, keys);
            Assert.Equal(expected, dict.Get(key));
            Assert.True(CheckInvariants(dict));
        }

        [Theory]
        [InlineData(new string[] { "a", "b", "c", "d" }, 3, 6)]
        [InlineData(new string[] { "a", "b", "c", "d", "e", "f" }, 4, 8)]
        public void TestRealloc(string[] keys, int startSize, int expectedSize)
        {
            NativeDictionary<string> dict = new(startSize);
            foreach (string key in keys)
                dict.Put(key, $"v-{key}");

            Assert.Equal(expectedSize, dict.size);
            foreach (string key in keys)
                Assert.Equal($"v-{key}", dict.Get(key));
            Assert.True(CheckInvariants(dict));
        }

        [Theory]
        [InlineData(new string[] { "a", "b", "c" }, "a", true)]
        [InlineData(new string[] { "a", "b", "c" }, "x", false)]
        [InlineData(new string[] { "" }, "", true)]
        public void TestIsKey(string[] keys, string key, bool expected)
        {
            NativeDictionary<string> dict = DictFromValues(5, keys);
            Assert.Equal(expected, dict.IsKey(key));
        }
    }
}
