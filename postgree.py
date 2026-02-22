import psycopg2

# Данные для подключения (проверь порт и пароль!)
conn_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123456789",  # Твой пароль из pgAdmin
    "host": "127.0.0.1",
    "port": "12345"             # ИСПРАВИЛИ: в PostgreSQL порт всегда 5432
}

def run_crud():
    conn = None
    try:
        # 1. ПОДКЛЮЧЕНИЕ
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        print("--- Успешное подключение к PostgreSQL ---")

        # 2. CREATE (Создание таблицы)
        cur.execute("CREATE TABLE IF NOT EXISTS my_crud_table (id SERIAL PRIMARY KEY, task_name TEXT);")
        cur.execute("INSERT INTO my_crud_table (task_name) VALUES (%s);", ("Сделать домашку по Python",))
        conn.commit() # ТРАНЗАКЦИЯ: сохраняем изменения
        print("C (Create): Таблица создана, данные в PostgreSQL отправлены.")

        # 3. READ (Чтение из базы)
        cur.execute("SELECT * FROM my_crud_table;")
        row = cur.fetchone()
        print(f"R (Read): Получено из базы -> {row}")

        # 4. UPDATE (Обновление в базе)
        cur.execute("UPDATE my_crud_table SET task_name = %s WHERE id = %s;", ("Домашка СДЕЛАНА!", row[0]))
        conn.commit() # ТРАНЗАКЦИЯ: сохраняем
        print("U (Update): Данные в PostgreSQL обновлены.")

        # 5. DELETE (Удаление)
        cur.execute("DELETE FROM my_crud_table WHERE id = %s;", (row[0],))
        conn.commit() # ТРАНЗАКЦИЯ: сохраняем
        print("D (Delete): Запись из PostgreSQL удалена.")

    except Exception as e:
        print(f"Ошибка! Скорее всего неверный пароль или порт: {e}")
        if conn:
            conn.rollback() # Если ошибка, отменяем всё, чтобы не поломать базу
    finally:
        if conn:
            cur.close()
            conn.close()
            print("--- Соединение закрыто ---")

if __name__ == "__main__":
    run_crud()