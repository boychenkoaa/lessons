namespace AlgorithmsDataStructures
{
    public class LinkedList2Tests
    {
        [Fact]
        public void TestAddInTail()
        {
            var list = new LinkedList2();
            // [] => 10
            list.AddInTail(new Node(10));
            Assert.Equal(1, list.Count());
            Assert.Equal(10, list.tail.value);

            // 10 => 10 20
            list.AddInTail(new Node(20));
            Assert.Equal(2, list.Count());
            Assert.Equal(10, list.head.value);
            Assert.Equal(20, list.head.next.value);
            Assert.Equal(20, list.tail.value);

            // 10 20 => 10 20 30
            list.AddInTail(new Node(30));
            Assert.Equal(3, list.Count());
            Assert.Equal(10, list.head.value);
            Assert.Equal(20, list.head.next.value);
            Assert.Equal(30, list.tail.value);
        }

        [Theory]
        [InlineData(new int[] { }, 10, new int[] { 10 })]
        [InlineData(new int[] { 10 }, 10, new int[] { 10, 10 })]
        [InlineData(new int[] { 20 }, 10, new int[] { 10, 20 })]
        [InlineData(new int[] { 20, 30, 40, 50 }, 10, new int[] { 10, 20, 30, 40, 50 })]
        public void TestAddInHead(int[] src, int _value, int[] _result)
        {
            var list = new LinkedList2();
            list.FromArray(src);
            list.AddInHead(new Node(_value));
            int[] result_arr = list.ToArray();
            Assert.True(result_arr.SequenceEqual(_result));
        }

        [Fact]
        public void TestIsEmpty()
        {
            var list = new LinkedList2();
            Assert.True(list.IsEmpty());
        }

        [Theory]
        [InlineData(new int[] { }, 10)]
        [InlineData(new int[] { 20 }, 20)]
        [InlineData(new int[] { 10, 20 }, 20)]
        [InlineData(new int[] { 10, 20, 30, 40, 50, 10, 20, 30, 40, 50 }, 10)]
        [InlineData(new int[] { 10, 20, 30, 40, 50, 10, 20, 30, 40, 50 }, 20)]
        [InlineData(new int[] { 10, 20, 30, 40, 50, 10, 20, 30, 40, 50 }, 30)]
        [InlineData(new int[] { 10, 20, 30, 40, 50, 10, 20, 30, 40, 50 }, 40)]
        [InlineData(new int[] { 10, 20, 30, 40, 50, 10, 20, 30, 40, 50 }, 50)]

        public void TestFind(int[] src, int _value)
        {
            LinkedList2 list = new LinkedList2();
            list.FromArray(src);

            Node node = list.Find(_value);
            if (src.Contains(_value))
            {
                Assert.Equal(_value, node.value);
            }
            else
            {
                Assert.Null(node);
            }
        }


        [Theory]
        [InlineData(new int[] { }, 10, new int[] { })]
        [InlineData(new int[] { 10 }, 10, new int[] { 10 })]
        [InlineData(new int[] { 10, 20, 30 }, 10, new int[] { 10 })]
        [InlineData(new int[] { 10, 20, 10, 10, 30, 10 }, 10, new int[] { 10, 10, 10, 10 })]
        [InlineData(new int[] { 20, 10, 10, 30, 10, 10 }, 10, new int[] { 10, 10, 10, 10 })]
        [InlineData(new int[] { 20, 30, 40, 50 }, 10, new int[] { })]
        [InlineData(new int[] { 20 }, 10, new int[] { })]
        public void TestFindAll(int[] src, int _value, int[] _result)
        {
            var list = new LinkedList2();
            list.FromArray(src);
            List<Node> result = list.FindAll(_value);
            int N = result.Count;
            int[] result_arr = result.Select(node => node.value).ToArray();
            Assert.True(result_arr.SequenceEqual(_result));
        }

        [Theory]
        [InlineData(new int[] { }, 10, new int[] { }, false)]
        [InlineData(new int[] { 10 }, 10, new int[] { }, true)]
        [InlineData(new int[] { 20 }, 10, new int[] { 20 }, false)]
        [InlineData(new int[] { 10, 10 }, 10, new int[] { 10 }, true)]
        [InlineData(new int[] { 10, 10, 10, 10, 10 }, 10, new int[] { 10, 10, 10, 10 }, true)]
        [InlineData(new int[] { 10, 20, 30 }, 10, new int[] { 20, 30 }, true)]
        [InlineData(new int[] { 10, 10, 20, 10, 30, 10, 10 }, 10, new int[] { 10, 20, 10, 30, 10, 10 }, true)]
        [InlineData(new int[] { 20, 30, 10, 10, 10 }, 10, new int[] { 20, 30, 10, 10 }, true)]
        [InlineData(new int[] { 20, 30, 20, 30, 20, 30 }, 10, new int[] { 20, 30, 20, 30, 20, 30 }, false)]

        public void TestRemove(int[] src, int _value, int[] target, bool _result)
        {
            LinkedList2 list = new LinkedList2();
            list.FromArray(src);
            bool result = list.Remove(_value);
            Assert.True(target.SequenceEqual(list.ToArray()));
            Assert.Equal(result, _result);
        }

        [Theory]
        [InlineData(new int[] { }, 10, new int[] { })]
        [InlineData(new int[] { 10 }, 10, new int[] { })]
        [InlineData(new int[] { 20 }, 10, new int[] { 20 })]
        [InlineData(new int[] { 10, 10 }, 10, new int[] { })]
        [InlineData(new int[] { 10, 10, 10, 10, 10 }, 10, new int[] { })]
        [InlineData(new int[] { 10, 20, 30 }, 10, new int[] { 20, 30 })]
        [InlineData(new int[] { 10, 10, 20, 10, 30, 10, 10 }, 10, new int[] { 20, 30 })]
        [InlineData(new int[] { 20, 30, 10, 10, 10 }, 10, new int[] { 20, 30 })]
        [InlineData(new int[] { 10, 10, 10, 10, 20, 30 }, 10, new int[] { 20, 30 })]
        [InlineData(new int[] { 20, 30, 20, 30, 20, 30 }, 10, new int[] { 20, 30, 20, 30, 20, 30 })]

        public void TestRemoveAll(int[] src, int value, int[] target)
        {
            LinkedList2 list = new LinkedList2();
            list.FromArray(src);
            list.RemoveAll(value);
            Assert.True(target.SequenceEqual(list.ToArray()));
        }

        [Theory]
        [InlineData(new int[] { })]
        [InlineData(new int[] { 10 })]
        [InlineData(new int[] { 10, 20 })]
        [InlineData(new int[] { 10, 20, 30 })]
        public void TestClear(int[] arr)
        {
            var list = new LinkedList2();
            list.FromArray(arr);
            list.Clear();
            Assert.True(list.IsEmpty());
        }

        [Theory]
        [InlineData(new int[] { }, 0)]
        [InlineData(new int[] { 10 }, 1)]
        [InlineData(new int[] { 10, 20 }, 2)]
        [InlineData(new int[] { 10, 20, 30 }, 3)]
        public void TestCount(int[] arr, int target)
        {
            var list = new LinkedList2();
            list.FromArray(arr);
            Assert.Equal(target, list.Count());
        }

        [Theory]
        [InlineData(new int[] { 10 }, 10, 20, new int[] { 10, 20 })]
        [InlineData(new int[] { 10, 10 }, 10, 20, new int[] { 10, 20, 10 })]
        [InlineData(new int[] { 10, 20, 30, 40 }, 10, 20, new int[] { 10, 20, 20, 30, 40 })]
        [InlineData(new int[] { 10, 20, 30, 40 }, 40, 50, new int[] { 10, 20, 30, 40, 50 })]
        public void TestInsertAfterNotNull(int[] src, int value_after, int value, int[] target)
        {
            LinkedList2 list = new LinkedList2();
            list.FromArray(src);
            Node node_after = list.Find(value_after);
            list.InsertAfter(node_after, new Node(value));
            Assert.True(list.ToArray().SequenceEqual(target));
        }

        [Theory]
        [InlineData(new int[] { }, 10, new int[] { 10 })]
        [InlineData(new int[] { 20 }, 10, new int[] { 10, 20 })]
        [InlineData(new int[] { 20, 30, 40 }, 10, new int[] { 10, 20, 30, 40 })]
        public void TestInsertAfterNull(int[] src, int value, int[] target)
        {
            LinkedList2 list = new LinkedList2();
            list.FromArray(src);
            list.InsertAfter(null, new Node(value));
            Assert.True(list.ToArray().SequenceEqual(target));
        }

        [Fact]
        public void TestFromArray()
        {
            var list = new LinkedList2();
            int[] arr = { 10, 20, 30, 40, 50 };
            list.FromArray(arr);
            Assert.Equal(5, list.Count());
            Assert.Equal(10, list.head.value);
            Assert.Equal(20, list.head.next.value);
            Assert.Equal(30, list.head.next.next.value);
            Assert.Equal(40, list.head.next.next.next.value);
            Assert.Equal(50, list.head.next.next.next.next.value);
            Assert.Equal(50, list.tail.value);
        }

        [Theory]
        [InlineData(new int[] { })]
        [InlineData(new int[] { 1 })]
        [InlineData(new int[] { 1, 2, 3 })]
        [InlineData(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 })]
        public void TestFromToArrayInv(int[] arr)
        {
            LinkedList2 list = new LinkedList2();
            list.FromArray(arr);
            int[] new_arr = list.ToArray();
            Assert.True(arr.SequenceEqual(new_arr));

        }
    }
}
