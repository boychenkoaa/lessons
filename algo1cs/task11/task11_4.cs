namespace AlgorithmsDataStructures
{
    
    public class UnitTest11_4
    {
        private string[] STRINGS_10 =
        new string[]
        {"0123456789", "1234567890", "2345678901", "3456789012", "4567890123", 
        "5678901234", "6789012345", "7890123456", "8901234567", "9012345678"};

        private static int[] CloneCounts(BloomFilterCount filter)
        {
            int[] ans = new int[BloomFilterCount.FILTER_LEN];
            for (int i = 0; i < BloomFilterCount.FILTER_LEN; i++)
                ans[i] = filter.FilterCounts[i];
            return ans;
        }

        [Fact]
        public void TestAdd()
        {
            // добавляем строки тестового набора
            
            BloomFilterCount filter = new();
            foreach (string s in STRINGS_10)
                filter.Add(s);
            
            // сверяем мультимножество с эталоном
            int [] counts = new int[32];
            for (int i = 0; i < 32; i++)
                counts[i] = 0;

            counts[5] = 5;
            counts[13] = 5;
            counts[27] = 5;
            counts[29] = 5;
            for (int i = 0; i < 32; i++)
                Assert.Equal(filter.FilterCounts[i], counts[i]);

            // проверяем инвариант - нет ложноотрицательных срабатываний
            foreach (string s in STRINGS_10)
                Assert.True(filter.Has(s));

        }

        [Fact]
        public void TestRemove()
        {
            BloomFilterCount filter = new();
            foreach (string s in STRINGS_10)
                filter.Add(s);

            string toRemove = STRINGS_10[0];
            int[] before = CloneCounts(filter);
            int hash1 = filter.Hash1(toRemove);
            int hash2 = filter.Hash2(toRemove);

            filter.Remove(toRemove);
            // проверяем что нет удаленной -- правда, придется перебрать элементы полностью
            Assert.False(filter.Has(toRemove));
            // проверяем что не удалились остальные
            for (int i = 1; i < STRINGS_10.Length; i++)
                Assert.True(filter.Has(STRINGS_10[i]));

            // проверяем разницу -- что отличаются на 1
            int[] expectedDelta = new int[BloomFilterCount.FILTER_LEN];
            expectedDelta[hash1]++;
            expectedDelta[hash2]++;
            for (int i = 0; i < BloomFilterCount.FILTER_LEN; i++)
                Assert.Equal(before[i] - expectedDelta[i], filter.FilterCounts[i]);
            
            // удаляем еще раз ту же строку и убеждаемся, что ничего не произошло
            int[] afterFirstRemove = CloneCounts(filter);
            filter.Remove(toRemove);
            for (int i = 0; i < BloomFilterCount.FILTER_LEN; i++)
                Assert.Equal(afterFirstRemove[i], filter.FilterCounts[i]);
        }

        [Fact]
        public void TestMerge()
        {
            
            // делим на две половинки и проверяем что все элементы в слитом массиве есть
            // ну и естественно проверяем почленное суммирование
            BloomFilterCount left = new();
            BloomFilterCount right = new();

            for (int i = 0; i < 5; i++)
                left.Add(STRINGS_10[i]);
            for (int i = 5; i < STRINGS_10.Length; i++)
                right.Add(STRINGS_10[i]);

            int[] leftBefore = CloneCounts(left);
            int[] rightBefore = CloneCounts(right);

            left.Merge(right);
            // проверяем почленное суммирование
            for (int i = 0; i < BloomFilterCount.FILTER_LEN; i++)
                Assert.Equal(leftBefore[i] + rightBefore[i], left.FilterCounts[i]);
            
            // проверяем объединение
            foreach (string s in STRINGS_10)
                Assert.True(left.Has(s));
        }
    }
}
