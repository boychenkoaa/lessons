using System;
using System.Collections.Generic;
using Xunit;

namespace AlgorithmsDataStructures
{
    public class UnitTest9_4
    {
        [Fact]
        public void TestAddAndGet()
        {
            NativeDictionary3<string> dict = new();
            dict.Add("a", "va");
            dict.Add("b", "vb");

            Assert.Equal("va", dict.GetItem("a"));
            Assert.Equal("vb", dict.GetItem("b"));
        }

        [Fact]
        public void TestReplaceValueByKey()
        {
            NativeDictionary3<string> dict = new();
            dict.Add("a", "va");
            dict.Add("a", "va2");

            Assert.Equal("va2", dict.GetItem("a"));
        }

        [Fact]
        public void TestRemove()
        {
            NativeDictionary3<string> dict = new();
            dict.Add("a", "va");
            dict.Remove("a");

            Assert.Null(dict.GetItem("a"));
        }

        [Fact]
        public void TestRemoveMissingThrows()
        {
            NativeDictionary3<string> dict = new();
            Assert.Throws<KeyNotFoundException>(() => dict.Remove("missing"));
        }

    }

    public class UnitTest9_4_Bin
    {
        [Fact]
        public void TestBinPutAndGet()
        {
            NativeDictionaryBin<string> dict = new(5);
            dict.Put(1UL, "v1");
            dict.Put(2UL, "v2");

            Assert.Equal("v1", dict.Get(1UL));
            Assert.Equal("v2", dict.Get(2UL));
        }

        [Fact]
        public void TestBinReplaceValueByKey()
        {
            NativeDictionaryBin<string> dict = new(3);
            dict.Put(1UL, "v1");
            dict.Put(1UL, "v1b");

            Assert.Equal("v1b", dict.Get(1UL));
        }

        [Fact]
        public void TestBinIsKey()
        {
            NativeDictionaryBin<string> dict = new(3);
            dict.Put(10UL, "v10");

            Assert.True(dict.IsKey(10UL));
            Assert.False(dict.IsKey(11UL));
        }

        [Fact]
        public void TestBinReallocKeepsValues()
        {
            NativeDictionaryBin<string> dict = new(2);
            dict.Put(1UL, "v1");
            dict.Put(3UL, "v3");
            dict.Put(5UL, "v5");

            Assert.Equal(4, dict.size);
            Assert.Equal("v1", dict.Get(1UL));
            Assert.Equal("v3", dict.Get(3UL));
            Assert.Equal("v5", dict.Get(5UL));
        }

        [Fact]
        public void TestBinGetMissingReturnsDefault()
        {
            NativeDictionaryBin<string> dict = new(3);
            Assert.Null(dict.Get(99UL));
        }
    }
}
