from typing import List, Dict


class Matcher:
    """Класс для сопоставления товара с запросами на основе релевантности."""
    def match(self, products: List[Dict], queries: List[str]) -> List[Dict]:
        """Сопоставляет продукты с запросами, рассчитывает релевантность
        и возвращает топ-10 релевантных продуктов."""
        results = []
        for product in products:
            text = (product["title"] + " " + product["description"]).lower()
            relevance = 0
            for query in queries:
                query_words = query.lower().split()
                for word in query_words:
                    if word in text.split():
                        relevance += 1
            results.append(
                {
                    "id": product["id"],
                    "title": product["title"],
                    "description": product["description"],
                    "category": product["category"],
                    "relevance": relevance,
                }
            )
        # Ранжировать по релевантности (от большему)
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:10]  # Топ-10
