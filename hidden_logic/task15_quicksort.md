Реализация быстрой сортировки:

```
using System.Collections.Generic;

int partition(arrst<int> arr, int left, int right)
{
    int pivot = arr[right];
    int i = left;

    for (int j = left; j < right; j++)
    {
        if (arr[j] < pivot)
        {

            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            i++;
        }
    }
    int temp = arr[i];
    arr[i] = arr[right];
    arr[right] = temp;
    return i;
}

void quicksort_base(arrst<int> arr, int left, int right)
{
    if (left < right)
    {
        int pivotIndex = partition(arr, left, right);
        quicksort_base(arr, left, pivotIndex - 1);
        quicksort_base(arr, pivotIndex + 1, right);
    }
}

void quicksort(arrst<int> arr)
{
    quicksort_base(arr, 0, arr.Count - 1);
}
```

# Доказательство корректности
## Пред- и постусловия для функций
Сформулируем пред- и постусловия для всех трех функций

**partition**
- `{P: left < right} `
- `result = partition(arr, left, right) `
- ```{Q:  (∀k ∈ [left, result-1]: arr[k] ≤ arr[result]) ∧  (∀k ∈ [result+1, right]: arr[k] ≥ arr[result]) ∧  (arr[result] = old(arr[right]))}```

**quicksort_base**
- `{P: left < right}` 
- `quicksort_base(arr, left, right) `
- `{Q: ∀i,j: left ≤ i ≤ j ≤ right ⇒ arr[i] ≤ arr[j]}`

**quicksort**
- `{P: true}`
- `quicksort(arr) `
- `{Q: ∀i,j: 0 ≤ i ≤ j < arr.Count ⇒ arr[i] ≤ arr[j]`

## Докажем корректность partition

### 1. Докажем инвариант цикла for (2 части постусловия из 3х):

``` 
I: ∀k ∈ [left, i-1]: arr[k] < pivot ∧ ∀k ∈ [i, j-1]: arr[k] ≥ pivot
```
**База**. 
- Перед циклом: i = left, j = left
- [left, i-1] = [left, left-1] = ∅
- [i, j-1] = [left, left-1] = ∅

"пустая истина"

**Индукционный переход для `j`-го элемента.
Пусть `I(i,j)` истинен перед проверкой `arr[j]`**.

**Случай 1: `arr[j] < pivot`**
1. Меняем `arr[i]` и `arr[j]` местами
2. `i++`
3. **Докажем `I(i+1, j+1)`**:
   - Для `k ∈ [left, i]`: 
     - Если `k ∈ [left, i-1]`: из `I(i,j)` знаем `arr[k] < pivot`
     - Если `k = i`: `arr[i]` (новый) = старый `arr[j]` `< pivot`
   - Для `k ∈ [i+1, j]`:
     - Если `k ∈ [i+1, j-1]`: из `I(i,j)` знаем `arr[k] ≥ pivot`
     - Если `k = j`: `arr[j]` (новый) = старый `arr[i]` 
       - Из `I(i,j)`: `∀k ∈ [i, j-1]: arr[k] ≥ pivot`
       - В частности, для `k = i`: старый `arr[i] ≥ pivot`
       - Значит, новый `arr[j] ≥ pivot`

**Случай 2: `arr[j] ≥ pivot`**
1. Ничего не меняем
2. Докажем `I(i, j+1)`
   - Для `k ∈ [left, i-1]`: из `I(i,j)` знаем `arr[k] < pivot`
   - Для `k ∈ [i, j]`:
     - Если `k ∈ [i, j-1]`: из `I(i,j)` знаем `arr[k] ≥ pivot`
     - Если `k = j`: `arr[j] ≥ pivot` по условию случая

### 2. Завершим доказательство корректности partition

Третью часть постусловия partition  `arr[result] = old(arr[right]) ` обеспечивает  обмен pivot и arr[result] местами после цикла (очевидно).

## Докажем корректность quicksort_base

Индукция по длине подмассива right-left

**База индукции**
если `left == right` (длина = 1), то массив отсортирован

**Индукционный переход**
пусть массивы длины `1..N-1` алгоритм сортирует корректно
тогда
1. в силу корректности partition, `∀k ∈ [left, pivotIndex-1]: arr[k] <= pivot`
2. в силу корректности partition, `∀k ∈ [pivotIndex+1, right]: arr[k] >= pivot`
3. в силу индукционного предположения, подмассивы `arr[left:pivotIndex-1]` и `arr[pivotIndex+1:right]` будут отсортированы корректно

## Докажем корректность quicksort
Очевидно, как частный случай `quicksort_base`
