from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List, Dict, Any
import motor.motor_asyncio

# --- Settings Management ---
# .env 파일로부터 환경 변수를 읽어오기 위한 설정 클래스
class Settings(BaseSettings):
    # 여기에 .env 파일에 정의할 변수들을 선언합니다.
    # 예: DATABASE_URL=mongodb+srv://<user>:<password>@<cluster-url>
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

# --- Database Setup (MongoDB) ---
# MongoDB 클라이언트를 생성합니다.
client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
# `devicemind` 라는 이름의 데이터베이스를 사용합니다.
db = client.devicemind

# --- Pydantic Models (API Data Validation) ---
# API 요청 본문의 구조를 정의하고 유효성을 검사합니다. (이전과 동일)
class AppUsageSchema(BaseModel):
    packageName: str
    totalTimeInForeground: int

class BatteryPerformanceSchema(BaseModel):
    level: float
    health: str
    status: str
    temperature: float
    voltage: float

class DeviceDataSchema(BaseModel):
    batteryPerformance: BatteryPerformanceSchema
    appUsage: List[AppUsageSchema]

# --- FastAPI App ---
app = FastAPI()

# FastAPI 앱이 시작될 때 MongoDB 연결을 확인합니다.
@app.on_event("startup")
async def startup_db_client():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "AI Logic Server is running with MongoDB"}

@app.post("/data/")
async def save_device_data(data: DeviceDataSchema):
    """
    Flutter 앱으로부터 디바이스 데이터를 받아서 MongoDB에 저장합니다.
    """
    try:
        # Pydantic 모델을 dictionary로 변환합니다.
        data_dict = data.dict()
        # 타임스탬프를 추가합니다.
        data_dict["timestamp"] = datetime.datetime.utcnow()

        # `snapshots` 라는 collection(SQL의 테이블과 유사)에 데이터를 삽입(insert)합니다.
        await db["snapshots"].insert_one(data_dict)
        
        return {"status": "success", "message": "Data saved successfully to MongoDB."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pydantic 모델이 datetime을 지원하도록 설정
from pydantic import ConfigDict
import datetime

DeviceDataSchema.model_config = ConfigDict(arbitrary_types_allowed=True)
