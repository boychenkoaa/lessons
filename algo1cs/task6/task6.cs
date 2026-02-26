using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

/*
2. Как можно понизить (выровнять) сложность addHead/removeHead и addTail/removeTail, 
с помощью какого ранее изученного типа данных?

Ответ: двусвязный список будет это делать за O(1), дальше понижать уже некуда
*/

namespace AlgorithmsDataStructures
{

  public class Deque<T>
  {
    LinkedList <T> linked_list;
    public Deque()
    {
     // инициализация внутреннего хранилища
     linked_list = new LinkedList<T>();
     }

  public bool IsEmpty => linked_list.First is null;

    public void AddFront(T item)
    {
     // добавление в голову
     linked_list.AddFirst(item);
    }

    public void AddTail(T item)
    {
     // добавление в хвост
     linked_list.AddLast(item);
    }

    public T RemoveFront()
    {
     // удаление из головы
      if (IsEmpty)
        return default(T);

      T ans = linked_list.First.Value;
      linked_list.RemoveFirst();
      return ans;
    }

    public T RemoveTail()
    {
     // удаление из хвоста
     if (IsEmpty)
        return default(T);

      T ans = linked_list.Last.Value;
      linked_list.RemoveLast();
      return ans;
    }
        
    public int Size()
    {
      return linked_list.Count;
    }

    public T First()
    {
      if (IsEmpty)
        return default(T);
      return linked_list.First.Value;
    }

    public T Last()
    {
      if (IsEmpty)
        return default(T);
      return linked_list.Last.Value;
    }
  }

}