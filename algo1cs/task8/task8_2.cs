namespace AlgorithmsDataStructures
{

    public class UnitTest8
    {
        // возвращает false, если таблица слишком мала либо элемент уже есть
        public static bool FillTable(HashTable table, string[] values)
        {
            foreach (string val in values)
            {
                if (table.Put(val) == -1)
                    return false;
            }
            return true;
        }

        public static bool IsEqTableSlots(HashTable table, string[] values)
        {
            HashSet<string> table_values = table.slots.Where(slot => slot is not null).ToHashSet();
            bool ans = values.ToHashSet().SetEquals(table_values);
            return ans;
        }

        [Theory()]
        [InlineData(new string[] { "a", "b", "c", "d", "e" }, 5, 2, true)]
        [InlineData(new string[] { "a", "b", "c", "d", "e" }, 5, 1, true)]
        [InlineData(new string[] { "a", "b", "c", "d", "e" }, 5, 3, true)]
        [InlineData(new string[] { "a", "b", "c", "d", "e" }, 4, 1, false)]
        [InlineData(new string[] { "a0", "a1", "a2", "a3", "a3", "a5" }, 5, 2, false)]
        [InlineData(new string[] { "a0", "a1", "a2", "a3", "a3", "a5" }, 5, 1, false)]
        [InlineData(new string[] { "a0", "a1", "a2", "a3", "a3", "a5" }, 6, 2, false)]
        [InlineData(new string[] { "a0", "a1", "a2", "a3", "a3", "a5" }, 6, 4, false)]
        [InlineData(new string[] { "a0", "a1", "a2", "a3", "a3", "a5" }, 6, 1, true)]
        [InlineData(new string[] { "a0", "a1", "a2", "a3", "a3", "a5" }, 6, 5, true)]
        public void TestPut(string[] values, int size, int step, bool ans)
        {
            HashTable table = new(size, step);
            bool fill_result = FillTable(table, values);
            Assert.Equal(ans, IsEqTableSlots(table, values));
            Assert.Equal(ans, fill_result);
        }

        [Theory()]
        [InlineData(new string[] { }, new string[] { "a", "b", "c", "d", "e" })]
        [InlineData(new string[] { "a", "b", "c", "d", "e" }, new string[] { "f", "g", "h" })]
        public void TestFind(string[] values, string[] values_ext)
        {
            HashTable table = new(values.Length == 0? 1: values.Length , 3);
            bool fill_result = FillTable(table, values);
            Assert.True(fill_result);
            Assert.True(values.All(value => table.Find(value) >= 0));
            Assert.Equal(values.Count(value => table.Find(value) >= 0), values.Length);
            Assert.True(values_ext.All(value => table.Find(value) == -1));
        }

        [Theory()]
        [InlineData(new string[] { "", "a", "b", "c", "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY" }, 11, 3)]
        [InlineData(new string[] { "a", "b", "c", "" }, 13, 2)]
        public void TestHashFun(string[] values, int size, int step)
        {
            HashTable table = new(size, step);
            foreach (string value in values)
            {
                Assert.True(table.HashFun(value) < size && table.HashFun(value) >= 0);
            }
        }



    }


}