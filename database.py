from sqlite3 import Connection, Cursor, connect
from datetime import datetime
from typing import Any


def create_db_connection() -> tuple[Connection, Cursor]:
    """Создает соединение с базой данных и возвращает его"""

    conn = connect('indicators_pc.db')
    cursor = conn.cursor()
    return conn, cursor


def create_db() -> None:
    """Функция для создания базыданных"""

    conn, cursor = create_db_connection()

    # Создаем таблицу показателями 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT, 
        indicators_use TEXT
    )
    ''')
    conn.commit()
    conn.close()


def add_indicators(cursor: Cursor, conn: Connection, indicators_use: str) -> None:
    """Функция для добавления записи показаний в таблицу"""

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO indicators (date, indicators_use)
    VALUES (?, ?)
    ''', (date, indicators_use))
    conn.commit()


def get_history() -> list[Any]:
    """Функция для получения данных истории показателей ПК"""

    conn, cursor = create_db_connection()
    
    # Получаем данные из бд
    cursor.execute('SELECT date, indicators_use FROM indicators')
    rows = cursor.fetchall()
    conn.close()
    
    return rows
