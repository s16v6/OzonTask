# Ozon-like Mini Service

Мини-сервис для загрузки данных с mock API, matching товаров и генерации отчетов.

## Установка
1. Клонировать репозиторий.
2. Виртуальное окружение: `python -m venv venv; source venv/bin/activate`.
3. Зависимости: `pip install -r requirements.txt`.
4. Поместить файлы в `mock_data/`: products_page_*.json, sales_*.json, queries.txt.

## Запуск
- Сервер: `python -m src.app, uvicorn src.app:app --reload`.
- Доступ: http://127.0.0.1:8000/report (JSON), /chart.png (PNG).
- Standalone: `python run.py` — загрузка и генерация файлов.

## Тесты
`pytest tests/`

## Trade-offs
- **SQLite**: В production нужна БД с индексами (е.g., PostgreSQL).
- **Matching**: Простой подсчет слов — быстро, но не учитывает семантику (TF-IDF или ML лучше для прод).
- **FastAPI**: Async не используется, так как синхронный — достаточно для мини-задачи.
- **График**: Matplotlib — статично, для веба можно Plotly.
- Логи и retry: Минимальны, но достаточны.
