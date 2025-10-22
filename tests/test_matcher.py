from src.matcher import Matcher


def test_match():
    products = [
        {
            "id": 1,
            "title": "Ozon интеграция",
            "description": "пример",
            "category": "Test",
        }
    ]
    queries = ["ozon интеграция"]
    matcher = Matcher()
    result = matcher.match(products, queries)
    assert len(result) == 1
    assert result[0]["relevance"] == 2  # Слова "ozon" и "интеграция" в title
