using Xunit;
using AlgorithmsDataStructures;

namespace AlgorithmsDataStructures
{
    public class LinkedListTests
    {
        [Fact]
        public void TestAddInTail()
        {
            var list = new LinkedList();
            list.AddInTail(new Node(10));
            Assert.Equal(1, list.Count());
        }

        [Fact]
        public void TestAddInHead()
        {
            var list = new LinkedList();
            list.AddInHead(new Node(10));
            Assert.Equal(1, list.Count());
        }

        [Fact]
        public void TestIsEmpty()
        {
            var list = new LinkedList();
            Assert.True(list.IsEmpty());
        }

        [Fact]
        public void TestFind()
        {
            var list = new LinkedList();
            list.AddInTail(new Node(10));
            var node = list.Find(10);
            Assert.NotNull(node);
            Assert.Equal(10, node.value);

            list = new LinkedList();
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(20));
            node = list.Find(15);
            Assert.Null(node);
        }

        [Fact]
        public void TestFindAll()
        {
            var list = new LinkedList();
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(10));
            var nodes = list.FindAll(10);
            Assert.Equal(2, nodes.Count);
        }

        [Fact]
        public void TestRemove()
        {
            var list = new LinkedList();
            list.AddInTail(new Node(10));
            var result = list.Remove(10);
            Assert.True(result);
            Assert.Equal(0, list.Count());
        }

        [Fact]
        public void TestRemoveAll()
        {
            var list = new LinkedList();
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(10));
            list.RemoveAll(10);
            Assert.True(list.IsEmpty());

            list = new LinkedList();
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(20));
            list.RemoveAll(10);
            Assert.Equal(list.head.value, 20);
            Assert.Equal(list.tail.value, 20);
            Assert.Equal(list.Count(), 1);

            list = new LinkedList();
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(20));
            list.AddInTail(new Node(20));
            list.AddInTail(new Node(20));
            list.RemoveAll(20);
            Assert.Equal(list.head.value, 10);
            Assert.Equal(list.tail.value, 10);
            Assert.Equal(list.Count(), 1);

            list = new LinkedList();
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(20));
            list.AddInTail(new Node(20));
            list.AddInTail(new Node(30));
            list.RemoveAll(20);
            Assert.Equal(10, list.head.value);
            Assert.Equal(30, list.tail.value);
            Assert.Equal(2, list.Count());
        }

        [Fact]
        public void TestClear()
        {
            var list = new LinkedList();
            Assert.True(list.IsEmpty());
            list.Clear();
            Assert.True(list.IsEmpty());
            list.AddInTail(new Node(10));
            list.AddInTail(new Node(20));
            list.Clear();
            Assert.True(list.IsEmpty());
        }

        [Fact]
        public void TestCount()
        {
            var list = new LinkedList();
            Assert.Equal(0, list.Count());
            list.AddInTail(new Node(10));
            Assert.Equal(1, list.Count());
            list.AddInHead(new Node(20));
            Assert.Equal(2, list.Count());
            list.Remove(10);
            Assert.Equal(1, list.Count());
            list.Remove(20);
            Assert.Equal(0, list.Count());
        }

        [Fact]
        public void TestInsertAfter()
        {
            var list = new LinkedList();
            list.AddInTail(new Node(10));
            var node = list.Find(10);
            list.InsertAfter(node, new Node(20));
            Assert.Equal(2, list.Count());
        }

    }
}
