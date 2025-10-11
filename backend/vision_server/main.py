from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
import cv2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Vision Server is running"}

@app.post("/analyze_phone/")
async def analyze_phone_exterior(file: UploadFile = File(...)):
    """
    업로드된 휴대폰 외관 이미지를 분석하여 상태 등급을 반환합니다.
    """
    # 파일이 이미지인지 확인
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    # 이미지 파일을 읽어서 OpenCV에서 사용할 수 있는 형태로 변환
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # --- OpenCV 분석 로직 (향후 구현) ---
    # 1. 이미지 전처리 (흑백 변환, 노이즈 제거 등)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. 흠집/파손 감지 (외곽선 감지, 임계 처리 등)
    # edges = cv2.Canny(gray, 50, 150)
    
    # 3. 정보 분석 및 등급 분류 (흠집 개수, 크기 등 계산)
    # defect_count = ...
    
    # -------------------------------------

    # 현재는 분석 로직이 없으므로, 임시로 더미 데이터를 반환합니다.
    grade = "A" # 임시 등급
    defects_found = 5 # 임시 흠집 개수

    return {
        "grade": grade,
        "defects_found": defects_found,
        "message": "Analysis logic is not yet implemented. This is a dummy response."
    }
