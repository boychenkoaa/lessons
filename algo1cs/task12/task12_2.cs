using Xunit;

namespace AlgorithmsDataStructures
{
    public class UnitTest12_2
    {
        [Fact]
        public void TestHasKeyValue()
        {
            var cache = new NativeCache<string>(3);

            cache.Push("a1", "10");
            cache.Push("b1", "20");
            cache.Push("c1", "30");

            Assert.Equal(3, cache.Count);
            Assert.True(cache.HasKey("a1"));
            Assert.True(cache.HasKey("b1"));
            Assert.True(cache.HasKey("c1"));
            Assert.False(cache.HasKey("x"));

            Assert.True(cache.HasValue("10"));
            Assert.True(cache.HasValue("20"));
            Assert.True(cache.HasValue("30"));
            Assert.False(cache.HasValue("999"));
        }

        [Fact]
        public void TestReplaceLastFreq()
        {
            var cache = new NativeCache<string>(2);

            cache.Push("a1", "A");
            cache.Push("b1", "B");
            // делаем самым популярным ключ a1
            Assert.Equal("A", cache.Get("a1"));
            Assert.Equal("A", cache.Get("a1"));

            cache.Push("c1", "C");

            // b1 самый редкий -- заместили его
            Assert.Equal(2, cache.Count);
            Assert.True(cache.HasKey("a1"));
            Assert.True(cache.HasKey("c1"));
            Assert.False(cache.HasKey("b1"));

            // 
            Assert.Equal("A", cache.Get("a1"));
            Assert.Equal("C", cache.Get("c1"));
            Assert.Null(cache.Get("b1"));
        }

        [Fact]
        public void TestPush()
        {
            var cache = new NativeCache<string>(max_count: 2);

            cache.Push("a1", "A");
            cache.Push("b1", "B");

            cache.Push("b1", "B2");

            cache.Push("c1", "C");

            Assert.Equal(2, cache.Count);
            Assert.False(cache.HasKey("a1"));
            Assert.True(cache.HasKey("b1"));
            Assert.True(cache.HasKey("c1"));

            Assert.Equal("B2", cache.Get("b1"));
            Assert.Equal("C", cache.Get("c1"));
            Assert.Null(cache.Get("a1"));
        }

        [Fact]
        public void TestPop()
        {
            var cache = new NativeCache<int>(max_count: 3);

            cache.Push("a1", 10);
            cache.Push("b1", 20);

            Assert.Equal(2, cache.Count);

            int removed = cache.Pop("a1");
            Assert.Equal(10, removed);
            Assert.Equal(1, cache.Count);
            Assert.False(cache.HasKey("a1"));
            Assert.True(cache.HasKey("b1"));

            int missing = cache.Pop("a1");
            Assert.Equal(default, missing);
            Assert.Equal(1, cache.Count);
        }
    }
}