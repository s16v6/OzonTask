from src.data_loader import DataLoader


def test_load_products():
    loader = DataLoader()
    products = loader.load_products()
    assert len(products) == 40  # Предполагается 2 страницы по 20
    assert "title" in products[0]


def test_load_sales():
    loader = DataLoader()
    sales = loader.load_sales()
    assert len(sales) > 0
    assert "product_id" in sales[0]


def test_load_queries():
    loader = DataLoader()
    queries = loader.load_queries()
    assert len(queries) == 6  # Из queries.txt
    assert "интеграция ozon" in queries
