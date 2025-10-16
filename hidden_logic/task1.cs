using Microsoft.EntityFrameworkCore;

public record StorageConnectionData(string Server, string Database, string User, string Password)
{
    public bool IsValid()
    {
        return !string.IsNullOrEmpty(Server) && 
               !string.IsNullOrEmpty(Database) && 
               !string.IsNullOrEmpty(User) && 
               !string.IsNullOrEmpty(Password);
    }
    public string GetConnectionString()
    {
        return $"Server={Server};Database={Database};User={User};Password={Password};";
    }

}

public class StrEntity
{
    public StrEntity(int id, string value)
    {
        this.id = id;
        this.value = value;
    }
    public int id { get; set; }
    public string value { get; set; }
}

public class Task1DbContext : DbContext
{
    private readonly StorageConnectionData _connection_data;

    public Task1DbContext(StorageConnectionData connection_data)
    {
        _connection_data = connection_data ?? throw new ArgumentNullException("connection_data");
    }
    public DbSet<StrEntity> task1table { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseMySql(
                _connection_data.GetConnectionString(),
                new MySqlServerVersion(new Version(8, 0, 43))
            );
        }
    }
}

interface Storage
{
    void save(string data);
    string retrieve(int id);
}

public class DBStorage
{
    private readonly StorageConnectionData _connection_data;

    public DBStorage(StorageConnectionData connection_data) 
    { 
        _connection_data = connection_data ?? throw new ArgumentNullException("connection_data");
    }
    public void save(string data)
    { 
        using (var context = new Task1DbContext(_connection_data))
        {
            int max_id = 0;
            if (context.task1table.Any()) 
            {
                max_id = context.task1table.Max(e => e.id);  
            }
            
            context.task1table.Add(new StrEntity(max_id+1, data));
            context.SaveChanges();

        }
    }

    public string retrieve(int id)
    {
        StrEntity result;
        using (var context = new Task1DbContext(_connection_data))
        {
            result = context.task1table.Find(id) ?? new StrEntity(0, "");
            
        }
        
        return result.value;
    }
}

public class App
{
    public static void Main()
    {
        var connection_data = new StorageConnectionData(
            Server: "localhost", 
            Database: "first", 
            User: "alex", 
            Password: "********"
        );

        var db_storage = new DBStorage(connection_data);
        db_storage.save("string 1");
        db_storage.save("string 2");
        string str1 = db_storage.retrieve(1);
        string str2 = db_storage.retrieve(2);
        Console.WriteLine(str1);
        Console.WriteLine(str2);
    }

}
