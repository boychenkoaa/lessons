using System;
using System.Collections.Generic;
/*
рефлексия на задание 9
9.5 решено верно
способ несколько иной -- сделал сначала OrderedSet на базе динамического массива
потом унаследовался от него классом KVOrderedSet, где переопределил метод Compare
А дальше уже сделал NativeDictionary3 как обертку над KVOrderedSet
Небольшое отличие было только в GetItem
*/

namespace AlgorithmsDataStructures
{
    /*
    11.2 -- слияние фильтров, реализован для фильтров с удалением, метод Merge
    просто почленно складываем массивы
    (для обычного фильтра это было бы логическое сложение двух масок)
    
    11.3 -- фильтр Блума с удалением
    основная идея: ведем массив счетчиков вместо битового массива. При добавлении увеличиваем, при удалении уменьшаем.
    Для предотвращения ложноположительных срабатываний ведем список значений.
        
    11.4 -- Поиск множества исходных значений фильтра Блума
    Не реализован.

    Однако, придумал реализуемое "на коленке" приближенное решение:
    1. Обозначаем множество поиска всех слов, которые могли туда попасть (большой список строк, например)
    Либо задаем его таким образом, чтобы можно было 1 к 1 восстановить номер слова.
    
    2. Стафим задачу оптимизации
    - Множество значений функции -- булевы векторы (единицы для включенных во множество элементов) с длиной, равной длине списка слов.
    - Функция = расстояние до эталонного фильтра по метрике L1 (сумма модулей разностей координат)
    
    3. Решаем задачу оптимизации
    3.1 Случайным образом выбираем начальное приближение
    3.2 Идем от него в сторону, где приближение лучше
    3.3 Повторяем до тех пор, пока не заберемся в локальный минимум
    
    3.5 пп 3.1--3.3 повторяем N раз (комбинация случайного поиска и жадного поиска)
    */

    public class BloomFilterCount
    {
        public const int FILTER_LEN = 32;
        public int[] FilterCounts = new int[FILTER_LEN];
        public List<string> values = new List<string>();

        public BloomFilterCount()
        {
            for (int i = 0; i < FILTER_LEN; i++)
                FilterCounts[i] = 0;
        }

        // хэш-функции
        public int Hash1(string str1)
        {
            // 17
            int ans = 0;
            for (int i = 0; i < str1.Length; i++)
            {
                int code = (int)str1[i];
                ans = (17 * ans + code) % FILTER_LEN;
            }
            return ans;
        }
        public int Hash2(string str1)
        {
            // 223
            // реализация ...
            int ans = 0;
            for (int i = 0; i < str1.Length; i++)
            {
                int code = (int)str1[i];
                ans = (223 * ans + code) % FILTER_LEN;
            }
            return ans;
        }

        public void Add(string str1)
        {
            // добавляем строку str1 в фильтр
            if (Has(str1))
                return;
            int hash1 = Hash1(str1);
            int hash2 = Hash2(str1);
            FilterCounts[hash1]++;
            FilterCounts[hash2]++;
            values.Add(str1);
        }

        public bool FilterHas(string str1)
        {
            // проверяем, есть ли строка str1 в фильтре
            int hash1 = Hash1(str1);
            int hash2 = Hash2(str1);
            return FilterCounts[hash1] > 0 && FilterCounts[hash2] > 0;
        }

        public bool Has(string str1)
        {
            return FilterHas(str1) && values.Contains(str1);
        }

        public void Remove(string str1)
        {
            if (Has(str1))
            {
                values.Remove(str1);
                int hash1 = Hash1(str1);
                int hash2 = Hash2(str1);
                FilterCounts[hash1]--;
                FilterCounts[hash2]--;
            }
        }

        public void Merge(BloomFilterCount other)
        {
            // классическое слияние фильтров -- почленное сложение мультимножеств
            for (int i = 0; i < FILTER_LEN; i++)
                FilterCounts[i] += other.FilterCounts[i];

            // а это особенности реализации -- у нас сами значения так же хранятся
            foreach (string str1 in other.values)
                values.Add(str1);
        }
    }
}
