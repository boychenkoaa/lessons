

## Задание
Дано
```
(1) 
{P: a = n, b = m} 
Max(a,b) 
{Q: res = 
n, n >= m; 
m, n < m }

(2) 
{P: a = n} 
Abs(a) 
{Q: res = {
n, n >= 0; 
-n, n < 0} 
}
```
Доказать, что 
```
{P: a = n, b = m} 
MaxAbs(a,b) 
{Q: res =
  n == m: n
  n > m >= 0: n
  m > n >= 0: m
  n >= 0, m < 0, n > -m: n
  n >= 0, m < 0, n < -m: m
  n < 0, m >= 0, m > -n: m
  n < 0, m >= 0, m < -n: n
  n < m <= 0: -n
  m < n <= 0: -m
}
```
### Доказательство
Возьмем два наглядных случая
```
1. Рассмотрим случай
n >= 0, m < 0, n > -m: n
Abs(n) = n, в силу n >= 0
Abs(m) = -m, в силу m < 0
Откуда MaxAbs(m, n) = Max(Abs(n), Abs(m)) = Max(n, -m) = n в силу того что n > -m

2. Рассмотрим случай
m < n <= 0: -m
Abs(m) = -m, в силу m < 0
Abs(n) = -n, в силу n <= 0
m < n => -m > -n
Откуда MaxAbs(m, n) = Max(Abs(m), Abs(n)) = Max(-m, -n) = -m

Остальные случаи доказываются аналогично
```
Код
```cs
public static int Max(int a, int b)
{
    return a >= b ? a : b;
}

public static int Abs(int a)
{
    return a >= 0 ? a : -a;
}

public static int MaxAbs(int a, int b):
{
  return Max(Abs(a), Abs(b))
}
```
