import json
import logging
import os
import time
import requests

from typing import List, Dict


logging.basicConfig(level=logging.INFO)


class DataLoader:
    """Загрузка данных о продуктах и продажах из локальных файлов JSON."""
    BASE_URL = os.path.join(os.path.dirname(__file__), "mock_data")

    def __init__(self, max_retries=3, timeout=5):
        self.max_retries = max_retries
        self.timeout = timeout
        self.start_date = "2025-09-01"
        self.end_date = "2025-09-02"

    def _load_with_retry(self, path: str) -> Dict:
        """
        Загружает данные из файла с повторными попытками при ошибках.
        Args:
            path (str): Путь к файлу для загрузки.
        Returns:
            Dict: Загруженные данные в виде словаря.
        """
        for attempt in range(self.max_retries):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logging.info(f"Loaded {path}")
                return data
            except (
                json.JSONDecodeError,
                FileNotFoundError,
                requests.exceptions.RequestException,
            ) as e:
                if (
                    isinstance(e, requests.exceptions.HTTPError)
                    and e.response.status_code == 429
                ):
                    wait_time = 2**attempt  # Exponential backoff
                    logging.warning(
                        f"429 Too Many Requests for {path}, retrying after {wait_time}s"
                    )
                    time.sleep(wait_time)
                else:
                    logging.error(f"Error loading {path}: {e}")
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(1)
        return {}

    def load_products(self) -> List[Dict]:
        """Загружает все продукты из страниценных JSON-файлов."""
        products = []
        page = 1
        while True:
            path = os.path.join(self.BASE_URL, f"products_page_{page}.json")
            if not os.path.exists(path):
                break
            data = self._load_with_retry(path)
            if "products" in data:
                products.extend(data["products"])
            page += 1
            logging.info(f"Loaded page {page-1}")
        return products

    def load_sales(self) -> List[Dict]:
        """Загружает продажи за указанный диапазон дат из JSON-файлов."""
        sales = []
        from datetime import datetime, timedelta

        current_date = datetime.fromisoformat(self.start_date)
        end_date_obj = datetime.fromisoformat(self.end_date)
        while current_date <= end_date_obj:
            date_str = current_date.strftime("%Y-%m-%d")
            path = os.path.join(self.BASE_URL, f"sales_{date_str}.json")
            if os.path.exists(path):
                data = self._load_with_retry(path)
                if isinstance(data, list):
                    sales.extend(data)
                logging.info(f"Loaded sales for {date_str}")
            current_date += timedelta(days=1)
        return sales

    def load_queries(self) -> List[str]:
        """Загружает список запросов из текстового файла."""
        path = os.path.join(self.BASE_URL, "queries.txt")
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
