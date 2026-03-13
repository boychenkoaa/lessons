using System.Linq;
using Xunit.Abstractions;

/*
минимальный набор тестов под доп задачи
писал ИИ, но я вижу
*/
namespace AlgorithmsDataStructures
{
    public class UnitTest8_4
    {
        private readonly ITestOutputHelper output;

        public UnitTest8_4(ITestOutputHelper output)
        {
            this.output = output;
        }

        private static string[] MakeValues(int count)
        {
            return Enumerable.Range(0, count).Select(i => $"v{i}").ToArray();
        }

        private static string[] MakeDdosValuesVaryLast(int count)
        {
            return Enumerable.Range(0, count)
                .Select(i => $"a{i:D3}{(char)('a' + (i % 26))}")
                .ToArray();
        }

        private static string[] MakeDdosValuesSameLast(int count)
        {
            return Enumerable.Range(1, count)
                .Select(i => "a" + new string('x', i) + "a")
                .ToArray();
        }

        [Fact]
        public void TestDynamicHashTablePutFind()
        {
            DynamicHashTable table = new(1);
            string[] values = MakeValues(20);

            foreach (string value in values)
                Assert.True(table.Put(value) >= 0);

            Assert.Equal(values.Length, table.Count);
            Assert.True(values.All(v => table.Find(v) >= 0));
            Assert.Equal(-1, table.Find("missing"));
        }

        [Fact]
        public void TestDynamicHashTableCollisions()
        {
            DynamicHashTable table = new(1);
            string[] values = { "a0", "a1", "a2", "a3", "a4" };

            foreach (string value in values)
                Assert.True(table.Put(value) >= 0);

            Assert.Equal(values.Length, table.Count);
            Assert.True(values.All(v => table.Find(v) >= 0));
        }

        [Fact]
        public void TestDynamicHashTableResizeKeepsItems()
        {
            DynamicHashTable table = new(1);
            string[] values = MakeValues(80);

            foreach (string value in values)
                Assert.True(table.Put(value) >= 0);

            Assert.Equal(values.Length, table.Count);
            Assert.True(values.All(v => table.Find(v) >= 0));
        }

        [Fact]
        public void TestDynamicHashTable2LinearProbingFind()
        {
            DynamicHashTable2 table = new();
            string[] values = { "b0", "b1", "b2", "b3", "b4", "b5" };

            foreach (string value in values)
                Assert.True(table.Put(value) >= 0);

            Assert.Equal(values.Length, table.Count);
            Assert.True(values.All(v => table.Find(v) >= 0));
            Assert.Equal(-1, table.Find("nope"));
        }

        [Fact]
        public void TestCountMatchesSlots()
        {
            DynamicHashTable table1 = new(1);
            string[] values1 = MakeValues(50);
            foreach (string value in values1)
                Assert.True(table1.Put(value) >= 0);
            Assert.Equal(table1.slots.Count(slot => slot is not null), table1.Count);

            DynamicHashTable2 table2 = new();
            string[] values2 = { "c0", "c1", "c2", "c3", "c4", "c5", "c6" };
            foreach (string value in values2)
                Assert.True(table2.Put(value) >= 0);
            Assert.Equal(table2.slots.Count(slot => slot is not null), table2.Count);
        }

        [Fact]
        public void TestDuplicateInsertsDoNotIncreaseCount()
        {
            DynamicHashTable table = new(1);
            Assert.True(table.Put("dup") >= 0);
            int countAfterFirst = table.Count;
            Assert.Equal(-1, table.Put("dup"));
            Assert.Equal(countAfterFirst, table.Count);
        }

        [Fact]
        public void TestCountAfterMultipleResizes()
        {
            DynamicHashTable table = new(1);
            string[] values = MakeValues(300);
            foreach (string value in values)
                Assert.True(table.Put(value) >= 0);
            Assert.Equal(values.Length, table.Count);
            Assert.True(values.All(v => table.Find(v) >= 0));
        }

        [Fact]
        public void TestDuplicateInsertsDoNotIncreaseCount2()
        {
            DynamicHashTable2 table = new();
            Assert.True(table.Put("dup2") >= 0);
            int countAfterFirst = table.Count;
            Assert.Equal(-1, table.Put("dup2"));
            Assert.Equal(countAfterFirst, table.Count);
        }

        [Fact]
        public void TestSecondHashReducesSeeks()
        {
            string[] values = MakeDdosValuesVaryLast(60);

            DynamicHashTable table1 = new(1);
            table1.DDoS(values);

            DynamicHashTable2 table2 = new();
            table2.DDoS(values);

            output.WriteLine($"Second hash seeks: {table1.SeeksCount}");
            output.WriteLine($"Linear probing seeks: {table2.SeeksCount}");
            output.WriteLine($"Second hash avg seeks: {(double)table1.SeeksCount / table1.Count:F2}");
            output.WriteLine($"Linear probing avg seeks: {(double)table2.SeeksCount / table2.Count:F2}");
            Assert.True(table1.SeeksCount < table2.SeeksCount);
        }

        [Fact]
        public void TestSaltReducesSeeks()
        {
            string[] values = MakeDdosValuesSameLast(60);

            DynamicHashTable tablePlain = new(1);
            tablePlain.DDoS(values);

            DynamicHashTable tableSalted = new(1);
            tableSalted.DDoSSalt(values);

            output.WriteLine($"Plain seeks: {tablePlain.SeeksCount}");
            output.WriteLine($"Salted seeks: {tableSalted.SeeksCount}");
            output.WriteLine($"Plain avg seeks: {(double)tablePlain.SeeksCount / tablePlain.Count:F2}");
            output.WriteLine($"Salted avg seeks: {(double)tableSalted.SeeksCount / tableSalted.Count:F2}");
            Assert.True(tableSalted.SeeksCount < tablePlain.SeeksCount);
        }
    }
}
