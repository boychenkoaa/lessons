using System.Reflection.Metadata;
using AlgorithmsDataStructures;

public class LinkedListTests
{
    [Fact]
    public void TestAddInTail()
    {
        var list = new LinkedList();
        // [] => 10
        list.AddInTail(new Node(10));
        Assert.Equal(1, list.Count());
        Assert.Equal(10, list.tail.value);
        
        // 10 => 10 20
        list.AddInTail(new Node(20));
        Assert.Equal(2, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(20, list.tail.value);

        // 10 20 => 10 20 30
        list.AddInTail(new Node(30));
        Assert.Equal(3, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(30, list.tail.value);
    }

    [Fact]
    public void TestAddInHead()
    {
        var list = new LinkedList();
        // [] => 10
        list.AddInHead(new Node(10));
        Assert.Equal(1, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(10, list.tail.value);

        // 10 => 20 10
        list.AddInHead(new Node(20));
        Assert.Equal(2, list.Count());
        Assert.Equal(20, list.head.value);
        Assert.Equal(10, list.tail.value);

        // 20 10 => 30 20 10
        list.AddInHead(new Node(30));
        Assert.Equal(3, list.Count());
        Assert.Equal(30, list.head.value);
        Assert.Equal(10, list.tail.value);
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
        // 10 => 10
        var list = new LinkedList();
        list.AddInTail(new Node(10));
        var node = list.Find(10);
        Assert.NotNull(node);
        Assert.Equal(10, node.value);

        // 10 20 => null
        list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        node = list.Find(15);
        Assert.Null(node);

        // 10 20 30 => null
        list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(30));
        node = list.Find(30);
        Assert.NotNull(node);
        Assert.Equal(30, node.value);
    }

    [Fact]
    public void TestFindAll()
    {
        // 10 10 => 10 10
        var list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(10));
        var nodes = list.FindAll(10);
        Assert.Equal(2, nodes.Count);

        // 10 10 => []
        nodes = list.FindAll(99);
        Assert.Empty(nodes);
        
        // [] => []
        list.Clear();
        nodes = list.FindAll(10);
        Assert.Empty(nodes);
        
        // 10 20 10 30 10 => 10 10 10
        list.Clear();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(30));
        list.AddInTail(new Node(10));
        nodes = list.FindAll(10);
        Assert.Equal(3, nodes.Count);

        // 10 20 10 30 10 => 20
        nodes = list.FindAll(20);
        Assert.Single(nodes);

        // singles
        list.Clear();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(30));
        list.AddInTail(new Node(40));
        list.AddInTail(new Node(50));
        nodes = list.FindAll(10);
        Assert.Single(nodes);
        nodes = list.FindAll(20);
        Assert.Single(nodes);
        nodes = list.FindAll(30);
        Assert.Single(nodes);
        nodes = list.FindAll(40);
        Assert.Single(nodes);
        nodes = list.FindAll(50);
        Assert.Single(nodes);


    }

    [Fact]
    public void TestRemove()
    {
        var list = new LinkedList();
        // 10 => [], true
        list.AddInTail(new Node(10));
        var result = list.Remove(10);
        Assert.True(result);
        Assert.Equal(0, list.Count());

        // [] => [], false
        list.Clear();
        result = list.Remove(10);
        Assert.False(result);
        Assert.Equal(0, list.Count());

        // 10 => 10, false
        list.Clear();
        list.AddInTail(new Node(10));
        result = list.Remove(20);
        Assert.False(result);
        Assert.Equal(1, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(10, list.tail.value);

        // 10 20 30 10 30 => 20 30 10 30, true
        list.Clear();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(30));
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(30));
        result = list.Remove(10);
        Assert.True(result);
        Assert.Equal(4, list.Count());
        Assert.Equal(20, list.head.value);
        Assert.Equal(30, list.tail.value);

        // 20 30 10 30 => 20 10 30
        result = list.Remove(30);
        Assert.True(result);
        Assert.Equal(3, list.Count());
        Assert.Equal(20, list.head.value);
        Assert.Equal(30, list.tail.value);

        // 20 10 30 => 20 10 30, false
        result = list.Remove(99);
        Assert.False(result);
        Assert.Equal(3, list.Count());
        Assert.Equal(20, list.head.value);
        Assert.Equal(30, list.tail.value);
        
        // 20 10 30 => 10 30, true
        result = list.Remove(20);
        Assert.True(result);
        Assert.Equal(2, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(30, list.tail.value);

        // 10 30 => 10
        result = list.Remove(30);
        Assert.True(result);
        Assert.Equal(10, list.head.value);
        Assert.Equal(10, list.tail.value);

        // 10 => []
        result = list.Remove(10);
        Assert.True(result);
        Assert.Null(list.head);
        Assert.Null(list.tail);


    }

    [Fact]
    public void TestRemoveAll()
    {
        // 10  => Empty
        var list = new LinkedList();
        list.AddInTail(new Node(10));
        list.RemoveAll(10);
        Assert.True(list.IsEmpty());
        
        // 10 10 10 => Empty
        list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(10));
        list.RemoveAll(10);
        Assert.True(list.IsEmpty());

        // 10 10 10 20 => 20
        list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.RemoveAll(10);
        Assert.Equal(20, list.head.value);
        Assert.Equal(20, list.tail.value);
        Assert.Equal(1, list.Count());

        // 10 20 20 20 => 10
        list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(20));
        list.RemoveAll(20);
        Assert.Equal(10, list.head.value);
        Assert.Equal(10, list.tail.value);
        Assert.Equal(1, list.Count());

        // 10 20 20 30 => 10 30
        list = new LinkedList();
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(30));
        list.RemoveAll(20);
        Assert.Equal(10, list.head.value);
        Assert.Equal(30, list.tail.value);
        Assert.Equal(2, list.Count());

        // 20 20 20 30 => 30
        list = new LinkedList();
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(20));
        list.AddInTail(new Node(30));
        list.RemoveAll(20);
        Assert.Equal(30, list.head.value);
        Assert.Equal(30, list.tail.value);
        Assert.Equal(1, list.Count());
    }

    [Fact]
    public void TestClear()
    {
        var list = new LinkedList();
        // []
        Assert.True(list.IsEmpty());
        
        // [] => []
        list.Clear();
        Assert.True(list.IsEmpty());
        
        // 10 20 => []
        list.AddInTail(new Node(10));
        list.AddInTail(new Node(20));
        list.Clear();
        Assert.True(list.IsEmpty());
    }

    [Fact]
    public void TestCount()
    {
        // []
        var list = new LinkedList();
        Assert.Equal(0, list.Count());
        
        // 10
        list.AddInTail(new Node(10));
        Assert.Equal(1, list.Count());
        
        // 20 10
        list.AddInHead(new Node(20));
        Assert.Equal(2, list.Count());
        
        // 20
        list.Remove(10);
        Assert.Equal(1, list.Count());
        
        // []
        list.Remove(20);
        Assert.Equal(0, list.Count());
    }

    [Fact]
    public void TestInsertAfter()
    {
        var list = new LinkedList();
        
        // Empty => 10
        // проверяем null-аргумент
        list.InsertAfter(null, new Node(10));
        Assert.Equal(1, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(10, list.tail.value);
        
        // проверяем вставку в конец
        // 10 => 10 20
        var node_after = list.Find(10);
        list.InsertAfter(node_after, new Node(20));
        Assert.Equal(2, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(20, list.tail.value);
        
        
        // проверяем вставку в конец
        // 10 20 => 10 20 30
        node_after = list.Find(20);
        list.InsertAfter(node_after, new Node(30));
        Assert.Equal(3, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(30, list.tail.value);

        // проверяем вставку в середину
        // 10 20 30 => 10 20 40 30
        node_after = list.Find(20);
        list.InsertAfter(node_after, new Node(20));
        Assert.Equal(4, list.Count());
        Assert.Equal(10, list.head.value);
        Assert.Equal(30, list.tail.value);

        // проверяем вставку в начало непустого списка
        // 10 20 40 30 => 50 10 20 40 30
        list.InsertAfter(null, new Node(50));
        Assert.Equal(5, list.Count());
        Assert.Equal(50, list.head.value);
        Assert.Equal(30, list.tail.value);
    }

}
