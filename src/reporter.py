import csv
import matplotlib.pyplot as plt

from typing import List, Dict


class Reporter:
    """Класс для генерации отчетов на основе продаж продуктов."""
    def generate_csv(self, products: List[Dict], sales: List[Dict]) -> str:
        """Генерирует CSV-файл с топ-продуктами по общим продажам."""
        top_products = []

        # Получаем продукты с общим продажами
        for product in products:
            total_sales = sum(
                s["qty"] * s["price"]
                for s in sales
                if s["product_id"] == product["id"]
            )
            top_products.append(
                {
                    "title": product["title"],
                    "category": product["category"],
                    "total_sales": total_sales,
                }
            )

        # Сортируем по total_sales по убыванию
        top_products.sort(key=lambda x: x["total_sales"], reverse=True)

        # Пишем в CSV
        with open("report.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["title", "category", "total_sales"]
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=","
                )
            writer.writeheader()
            writer.writerows(top_products)

        return "report.csv"

    def generate_chart(self, products: List[Dict], sales: List[Dict]) -> str:
        """Генерирует диаграмму топ-10 продуктов по общим продажам в PNG."""
        top_products = []

        # Получаем продукты с общим продажами
        for product in products:
            total_sales = sum(
                s["qty"] * s["price"]
                for s in sales
                if s["product_id"] == product["id"]
            )
            top_products.append(
                {"title": product["title"], "total_sales": total_sales}
                )

        # Сортируем по total_sales по убыванию
        top_products.sort(key=lambda x: x["total_sales"], reverse=True)

        # Берем топ-10
        top_10 = top_products[:10]

        # Данные для графика
        titles = [p["title"] for p in top_10]
        sales_values = [p["total_sales"] for p in top_10]

        # Строим бар-чарт
        plt.figure(figsize=(10, 6))
        plt.bar(titles, sales_values, color="skyblue")
        plt.xlabel("Product Title")
        plt.ylabel("Total Sales")
        plt.title("Top 10 Products by Total Sales")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Сохраняем в файл
        plt.savefig("chart.png")
        plt.close()  # Закрываем, чтобы не держать в памяти

        return "chart.png"
