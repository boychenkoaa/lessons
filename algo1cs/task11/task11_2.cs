using System;
using System.Collections.Generic;
using Xunit;

namespace AlgorithmsDataStructures
{
    public class UnitTest11
    {
        private string[] STRINGS_10 =
        new string[]
        {"0123456789", "1234567890", "2345678901", "3456789012", "4567890123", 
        "5678901234", "6789012345", "7890123456", "8901234567", "9012345678"};

        [Fact]
        public void TestAdd()
        {
            BloomFilter filter = new(32);
            foreach (string s in STRINGS_10)
                filter.Add(s);
            
            int bits = (1 << 5) | (1 << 13) | (1 << 27) | (1 << 29);
            Assert.Equal(filter.filter_bits, bits);
        }

        [Fact]
        public void TestIsValue()
        {
            BloomFilter filter = new(32);
            foreach (string s in STRINGS_10)
                filter.Add(s);

            // ложно-отрицательных быть не должно
            foreach (string s in STRINGS_10)
                Assert.True(filter.IsValue(s));
            
            // а ложноположительные возможны -- провоцируем
            // провоцируем ложноположительное срабатывание
            // от перестановки 0 и 2 символа хеш-коды не меняются
            foreach (string s in STRINGS_10)
            { 
                string s1 = String.Concat(s[2], s[1], s[0], s[3..]);
                Assert.True(filter.IsValue(s1));
            };
        }
    }
}