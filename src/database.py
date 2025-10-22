import sqlite3

from typing import List, Dict


class Database:
    """Класс для управления базой данных SQLite с продуктами и продажами."""
    DB_NAME = "ozon_data.db"

    def __init__(self):
        pass

    def _create_connection(self):
        conn = sqlite3.connect(
            self.DB_NAME, check_same_thread=False
        )  # check_same_thread=False для безопасности
        self._create_tables(conn)
        return conn

    def _create_tables(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                category TEXT
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                date TEXT,
                qty INTEGER,
                price REAL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """
        )
        conn.commit()

    def insert_products(self, products: List[Dict]):
        """Вставляет или обновляет список продуктов в базу данных."""
        conn = self._create_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT OR REPLACE INTO products (id, title, description, category) VALUES (?, ?, ?, ?)",
                [
                    (p["id"], p["title"], p["description"], p["category"])
                    for p in products
                ],
            )
            conn.commit()
        finally:
            conn.close()

    def insert_sales(self, sales: List[Dict]):
        """Вставляет список продаж в базу данных."""
        conn = self._create_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO sales (product_id, date, qty, price) VALUES (?, ?, ?, ?)",
                [(s["product_id"], s["date"], s["qty"], s["price"])
                 for s in sales
                 ],
            )
            conn.commit()
        finally:
            conn.close()

    def get_products(self) -> List[Dict]:
        """Получает список всех продуктов из базы данных."""
        conn = self._create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            results = [
                {"id": r[0],
                 "title": r[1],
                 "description": r[2],
                 "category": r[3]
                 }
                for r in cursor.fetchall()
            ]
            return results
        finally:
            conn.close()

    def get_sales(self) -> List[Dict]:
        """Получает список всех продаж из базы данных."""
        conn = self._create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT product_id, qty, price FROM sales")
            results = [
                {"product_id": r[0], "qty": r[1], "price": r[2]}
                for r in cursor.fetchall()
            ]
            return results
        finally:
            conn.close()

    def close(self):
        pass
