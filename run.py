import logging

from src.data_loader import DataLoader
from src.database import Database
from src.matcher import Matcher
from src.reporter import Reporter


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    loader = DataLoader()
    db = Database()
    matcher = Matcher()
    reporter = Reporter()

    products = loader.load_products()
    db.insert_products(products)

    sales = loader.load_sales()
    db.insert_sales(sales)

    queries = loader.load_queries()

    products_data = db.get_products()
    sales_data = db.get_sales()

    matched = matcher.match(products_data, queries)

    csv_path = reporter.generate_csv(matched, sales_data)
    chart_path = reporter.generate_chart(matched, sales_data)

    logging.info(f"Report generated: {csv_path}, Chart: {chart_path}")
    db.close()
