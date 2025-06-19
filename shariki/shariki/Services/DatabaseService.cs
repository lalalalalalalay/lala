using System;
using System.Collections.Generic;
using System.Data;
using Npgsql;

namespace BallCollisionWPF
{
    public class DatabaseService
    {
        private readonly string _connectionString;

        public DatabaseService(string connectionString)
        {
            _connectionString = connectionString;
            InitializeDatabase();
        }

        private void InitializeDatabase()
        {
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                conn.Open();
                using (var cmd = conn.CreateCommand())
                {
                    // Создаем таблицу, если не существует
                    cmd.CommandText = @"
                        CREATE TABLE IF NOT EXISTS Balls (
                            Id SERIAL PRIMARY KEY,
                            X DOUBLE PRECISION,
                            Y DOUBLE PRECISION
                        );";
                    cmd.ExecuteNonQuery();

                    // Если таблица пуста, вставляем стартовые позиции
                    cmd.CommandText = @"
                        INSERT INTO Balls (X, Y)
                        SELECT x, y FROM (VALUES (100,100),(200,150),(300,200),(400,250)) AS v(x,y)
                        WHERE NOT EXISTS (SELECT 1 FROM Balls);
                    ";
                    cmd.ExecuteNonQuery();
                }
            }
        }

        public List<(double X, double Y)> LoadInitialPositions()
        {
            var list = new List<(double X, double Y)>();
            using (var conn = new NpgsqlConnection(_connectionString))
            {
                conn.Open();
                using (var cmd = conn.CreateCommand())
                {
                    cmd.CommandText = "SELECT X, Y FROM Balls;";
                    using (var reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            list.Add((reader.GetDouble(0), reader.GetDouble(1)));
                        }
                    }
                }
            }
            return list;
        }
    }
}