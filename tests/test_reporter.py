import os
from src.reporter import Reporter


def test_generate_csv():
    reporter = Reporter()
    top = [
        {"id": 1,
         "title": "Test",
         "category": "Cat",
         "description": "",
         "relevance": 1
         }
    ]
    sales = [{"product_id": 1, "qty": 1, "price": 100}]
    path = reporter.generate_csv(top, sales)
    assert os.path.exists(path)
    os.remove(path)  # Cleanup


def test_generate_chart():
    reporter = Reporter()
    top = [
        {"id": 1,
         "title": "Test",
         "category": "Cat",
         "description": "",
         "relevance": 1
         }
    ]
    sales = [{"product_id": 1, "qty": 1, "price": 100}]
    path = reporter.generate_chart(top, sales)
    assert os.path.exists(path)
    os.remove(path)  # Cleanup
