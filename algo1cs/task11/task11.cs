using System.Collections.Generic;
using System;
using System.IO;

namespace AlgorithmsDataStructures
{
    public class BloomFilter
    {
        public int filter_len;
        public int filter_bits;

        public BloomFilter(int f_len)
        {
            // костыль, чтобы не использовать встроенный BitArray
            filter_len = 32;
            filter_bits = 0;
        }

        // хэш-функции
        public int Hash1(string str1)
        {
            // 17
            int ans = 0;
            for (int i = 0; i < str1.Length; i++)
            {
                int code = (int)str1[i];
                ans = (17 * ans + code) % filter_len;
            }
            return ans;
        }
        public int Hash2(string str1)
        {
            // 223
            int ans = 0;
            for (int i = 0; i < str1.Length; i++)
            {
                int code = (int)str1[i];
                ans = (223 * ans + code) % filter_len;
            }
            return ans;
        }

        public void Add(string str1)
        {
            // добавляем строку str1 в фильтр
            int hash1 = Hash1(str1);
            int hash2 = Hash2(str1);
            filter_bits |= 1 << hash1;
            filter_bits |= 1 << hash2;
        }

        public bool IsValue(string str1)
        {
            // проверка, имеется ли строка str1 в фильтре
            int hash1 = Hash1(str1);
            int hash2 = Hash2(str1);
            return (filter_bits & (1 << hash1)) != 0 && (filter_bits & (1 << hash2)) != 0;
        }
    }
}