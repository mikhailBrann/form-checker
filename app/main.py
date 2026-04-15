import uvicorn
from fastapi import FastAPI, Depends
from config.config import APP_CONFIG

# from routes.parse_data import router as parse_data_router
from services.parser_service import ParserService

app = FastAPI()

# app.include_router(
#     parse_data_router,
#     prefix="/import",
#     tags=["Импорт данных 📥"]
# )



if __name__ == "__main__":
    parser = ParserService()
    result = parser.parse_page_screenshot("https://site.ru/tula", "site_parse")
    print(result)
    
    # uvicorn.run(app, host="0.0.0.0", port=APP_CONFIG["APP_PORT"])