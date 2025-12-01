#nullable enable

class Point2D
{
    public float x { get; set; } = 0.0f;
    public float y { get; set; } = 0.0f;

    public static Point2D Clone(Point2D point)
    {
        if (point == null) return null;

        return new Point2D
        {
            x = point.x,
            y = point.y
        };
    }
}

// полилиния в функциональном стиле
public class Polyline2D
{
    public Point2D[] Points { get; private set; }

    public Polyline2D(Point2D[] points)
    {
        Points = points ?? Array.Empty<Point2D>();
    }

    // глубокая копия массива точек
    private static IEnumerable<Point2D> ClonePoints(IEnumerable<Point2D> points) =>
        points.Select(Clone);

    /*
    вставка
    предусловие: индекс от 0 до длины -1
    */
    public Polyline2D Insert(int index, Point2D newPoint)
    {
        ArgumentNullException.ThrowIfNull(newPoint);

        if (index < 0 || index > Points.Length)
            throw new ArgumentOutOfRangeException(nameof(index));
        var new_points = Points.Take(index)
              .Select(Clone)
              .Append(Clone(newPoint))
              .Concat(Points.Skip(index).Select(Clone))
              .ToArray();
        var result = Polyline2D(new_points);
        return result;
    }

    /* Удаление точки по индексу
     предусловие: полилиния не пуста и индекс в пределах 0..N-1
    */
    public Polyline2D Remove(int index)
    {
        if (Points.Length == 0)
            throw new InvalidOperationException("Polyline is empty");

        if (index < 0 || index >= Points.Length)
            throw new ArgumentOutOfRangeException(nameof(index));
        var new_points = Points.Where((_, i) => i != index)
            .Select(Clone)
            .ToArray();
        var result = new Polyline2D(new_points);
        return result;
    }

    // добавление в начало
    // предусловий нет
    public Polyline2D Prepend(Point2D newPoint)
    {
        ArgumentNullException.ThrowIfNull(newPoint);
        var new_points = new[] { Clone(newPoint) }.Concat(CloneAll(Points)).ToArray();
        var result = new Polyline2D(new_points);
        return result;
    }

    // добавление точки в конец
    // предусловий нет
    public Polyline2D Append(Point2D newPoint)
    {
        ArgumentNullException.ThrowIfNull(newPoint);
        var new_points = CloneAll(Points)
            .Append(Clone(newPoint))
            .ToArray();
        var result = new Polyline2D(new_points);
        return result;
    }

    // поиск первого вхождения по условию predicate
    public Polyline2D Filter(Func<Point2D, bool> predicate)
    {
        ArgumentNullException.ThrowIfNull(predicate);
        var new_points = Points.Where(predicate)
              .Select(Clone)
              .ToArray();
        var result = Polyline2D(new_points);
        return result;
    }

    // длина
    public float TotalLength()
    {
        if (Points.Length < 2) return 0f;
        var result = Points.Zip(Points.Skip(1), (a, b) =>
            MathF.Sqrt(
                MathF.Pow(b.x - a.x, 2) +
                MathF.Pow(b.y - a.y, 2)
            )
        ).Sum();
        return result;
    }

    // удаление дубликатов (сравниваем по значениям)
    public Polyline2D Distinct()
    {
        var seen = new HashSet<(float, float)>();
        new_points = Points.Where(p => seen.Add((p.x, p.y)))
              .Select(Clone)
              .ToArray();
        var result = Polyline2D(new_points);
        return result;
    }

    // реверс
    // без пред и постусловий
    public Polyline2D Reverse()
    {
        var result = Polyline2D(
            Points.Reverse()
                  .Select(Clone)
                  .ToArray()
        );
        return result;
    }

    // конкатенация
    public Polyline2D Concat(Polyline2D other)
    {
        ArgumentNullException.ThrowIfNull(other);

        var result = new Polyline2D(
            CloneAll(Points)
                .Concat(CloneAll(other.Points))
                .ToArray()
        );
        return result;
    }


    // количество точек (не путать с длиной)
    public int Count => Points.Length;

    // пустая или нет
    public bool IsEmpty => Points.Length == 0;
}
