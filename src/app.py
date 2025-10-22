import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from .data_loader import DataLoader
from .database import Database
from .matcher import Matcher
from .reporter import Reporter

logging.basicConfig(level=logging.INFO)


# Определяем lifespan (замена старого @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler: выполняет startup логику перед yield (как старый startup_event).
    """
    global PRODUCT_LOADED, SALES_LOADED, queries
    loader = DataLoader()
    db = Database()
    try:
        products = loader.load_products()
        db.insert_products(products)
        PRODUCT_LOADED = True
        logging.info("Products loaded")

        sales = loader.load_sales()
        db.insert_sales(sales)
        SALES_LOADED = True
        logging.info("Sales loaded")

        queries = loader.load_queries()
        logging.info("Queries loaded")
    except Exception as e:
        logging.error(f"Startup error: {e}")

    yield

app = FastAPI(lifespan=lifespan)


loader = DataLoader()
db = Database()
matcher = Matcher()
reporter = Reporter()

PRODUCT_LOADED = False
SALES_LOADED = False
queries = []


@app.get("/report")
def get_report() -> JSONResponse:
    """
    Эндпоинт для генерации отчета.
    Проверяет загрузку данных, выполняет сопоставление,
    генерирует CSV и график, возвращает топ-продукты в JSON.

    Returns:
        JSONResponse: JSON с топ-продуктами или ошибкой,
        если данные не загружены.
    """
    if not (PRODUCT_LOADED and SALES_LOADED):
        return JSONResponse({"error": "Data not loaded"})

    products = db.get_products()
    sales = db.get_sales()
    matched = matcher.match(products, queries)
    # Генерировать CSV и chart
    reporter.generate_csv(matched, sales)
    reporter.generate_chart(matched, sales)
    return JSONResponse({"top_products": matched})


@app.get("/chart.png")
def get_chart():
    """
    Эндпоинт для получения файла графика.
    Returns:
        FileResponse: Файл chart.png с типом media_type='image/png'.
    """
    return FileResponse("chart.png", media_type="image/png")
