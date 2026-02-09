using System;
using System.Reflection.Metadata.Ecma335;

/*
Рефлексия на задачи 2.
2.9
(+)
Все верно, единственное что head и tail меняются в начале и алгоритм итерируется назад по списку, а не вперед

2.10
(+/-)
У меня не ведется count как внутренне состояние (наоборот, конец списка используется при подсчете count)
Поэтму целостность проверял двойным циклом, за N^2 (фиксируем вершину и идем от нее либо до конца, либо до нее же
если нашлась вершина в которую вернулись -- мы нашли цикл)

2.11
(+)
Да, сортировка пузырьком подходит очень хорошо так как не надо обращаться к произвольному месту, 
зато надо менять местами два значения.

2.12
(+)
я не обобщал на N списков и не додумался до кучи, 
итеративно "в лоб" решил правильно
*/

namespace AlgorithmsDataStructures
{
    public class SuperStack
    {
        public Stack<float> stack = new();
        public Stack<float> stack_min = new();
        public Stack<float> stack_avg = new();

        public float MinFast()
        {
            return stack_min.Peek();
        }

        public float AVGFast()
        {
            return stack_avg.Peek();
        }

        public void Push(float elem)
        {
            stack.Push(elem);
            if (stack_min.IsEmpty)
            {
                stack_min.Push(elem);
                stack_avg.Push(elem);
                return;
            } 
            stack_min.Push(elem < stack_min.Peek() ? elem : stack_min.Peek());
            stack_avg.Push((stack_avg.Peek() * stack_avg.Size() + elem) / (stack_avg.Size() + 1));
        }

        public float Pop()
        {
            if (!stack.IsEmpty)
            {
                stack_avg.Pop();
                stack_min.Pop();
                return stack.Pop();
            }
            return default;
        }

        public static bool IsBracketsCorrect(string brackets)
        {
            Stack<char> bracketsStack = new();
            foreach (char c in brackets)
            {
                if (c == '(')
                {
                    bracketsStack.Push(c);
                    continue;
                }
                
                if (c != ')' || bracketsStack.IsEmpty)
                    return false;
                
                bracketsStack.Pop();
            }
            return true;
        }

        public static char LeftBracket(char rightBracket)
        {   
            char ans = rightBracket switch
            {
                ')' => '(',
                ']' => '[',
                '}' => '{',
                _ => '\0'
            };
            return ans;
        }
        public static bool IsBracketsCorrect2(string brackets)
        {
            Stack<char> bracketsStack = new();
            foreach (char c in brackets)
            {
                
                if (c is '(' or '{' or ']')
                {
                    bracketsStack.Push(c);
                    continue;
                }
                        
                char peek = bracketsStack.Peek();
                if (bracketsStack.IsEmpty || (LeftBracket(peek) != c))
                        return false;
                                
                if (peek != LeftBracket(c))
                    return false;

                bracketsStack.Pop();

            }
            return true;
        }

        public static int rpn(string s)
        {
            string [] parts = s.Split(',',   StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
            Stack<int> stack = new();
            foreach (string part in parts)
            {
                if ("+-*/".Contains(part))
                {
                    if (stack.Size() < 2)
                        throw new Exception("Incorrect input data");
                    
                    int op1 = stack.Pop();
                    int op2 = stack.Pop();
                    int res = part switch {
                        "+" => op1+op2,
                        "-" => op2-op1,
                        "*" => op1*op2,
                        "/" => op1/op2,
                        _ => throw new Exception("Incorrect input data")
                    };
                    stack.Push(res);
                    
                }
                else  
                {
                    int number = int.Parse(part);
                    stack.Push(number);
                }

            }
            if (stack.Size() != 1)
                throw new Exception("Incorrect input data");
            return stack.Peek();

        }
    }
}