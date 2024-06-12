from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as book_router
import certifi

# 환경 변수를 로드하고 가져올 수 있는 패키지
config = dotenv_values(".env")

app = FastAPI()

# 시작할때 실행되는 코드인가봐요
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client[config["DB_NAME"]]

# 종료할때 실행됨
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# tags는 api 문서의 태그를 변경해줍니다.
app.include_router(book_router, tags=["배고파"], prefix="/book")

