## Задачи 1 и 2 
-- я попался в обе ловушки (но я не джавист, мне можно, питончик бы отработал)

1. Не найдет метод `makesound` после изменения названия метода  у `Animal` -- `myCat` объявлен именно как `Animal`  (сначала я ответил "напечатает Meow")
2. Аналогично, метод `makesound(int numberOfSounds)` у `Animal` не определен -- ошибка.  (сначала я ответил "MeowMeowMeowMeow")

## Задача 3.  
(тут я уже углубился в джаву)
1. Конфликт зависимостей в системе сборки -- один и тот же пакет двух разных версий.
2. Видимость и время жизни переменной `result` ограничены блоками `try` , во втором блоке `result` переменная не объявлена / инициализирована, в первом пропала зря. Решение -- вынести ее на уровень выше.
3.  Парсинг `Map<String, Object> result = objectMapper.readValue(jsonString, HashMap.class);` я бы конкретизировал структуру, которую хочу увидеть на выходе (`Map<String, Object>` -- максимально общо). 

 объявил бы User как POJO (публичные поля исключительно для краткости записи)
```java
 public class User {
    // Публичные поля (Jackson может работать и с ними)
    public String name;
    public int age;

    public SimpleUserPublic(String name, int age) {
        this.name = name;
        this.age = age;
    }

}
```

и парсил бы в него
```java
User user = User("Alice", 24)
try {
    User user = mapper.readValue(json, User.class);
}
catch (...) {
    ...
}
