from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from openai import OpenAI
from dotenv import load_dotenv
import os

# 1. 환경 변수 로드 (.env 파일에서 OPENAI_API_KEY를 가져옴)
load_dotenv()

# OpenAI 클라이언트 초기화
# .env 파일에 OPENAI_API_KEY=sk-... 형태로 키가 저장되어 있어야 합니다.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. 경로 동적 계산 (기존 로직 유지)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONT_DIR = BASE_DIR / "a01_front"

print("기본 경로:", BASE_DIR)
print("FRONT 경로:", FRONT_DIR)

# 3. 템플릿 엔진에 계산된 프론트엔드 디렉토리 등록
templates = Jinja2Templates(directory=str(FRONT_DIR))

app = FastAPI()

# http://localhost:8000/tellGpt
@app.get("/tellGpt")
async def loginFrm(request: Request):
    msg = request.query_params.get("msg")
 
    msg1 = ""
    # 질문이 없을 경우 처리
    if not msg:
        return templates.TemplateResponse(
            request=request, 
            name="a01_showMsg.html", 
            context={"rstMsg": "질문을 입력해주세요."}
        )


    try:
        # app.chat이 아닌 client.chat으로 수정
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 친절하고 전문적인 IT 교육 도우미 챗봇입니다. 학생들이 프로그래밍 개념을 쉽게 이해할 수 있도록 명확하고 간결하게 설명해주세요."
                },
                {"role": "user", "content": msg}
            ],
            temperature=0.7
        )
        msg1 = response.choices[0].message.content

    except Exception as e:
        # 에러가 났을 때 화면에 보여줄 메시지를 msg1에 담도록 수정
        msg1 = f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}"

    # 정상 결과든 에러 결과든 msg1을 화면으로 전달
    return templates.TemplateResponse(
        request=request, 
        name="a01_showMsg.html", 
        context={"rstMsg": msg1}
    )

# 4. main() 실행시, 메모리에 로딩할 코드 처리..
if __name__ == "__main__":
    # 서버 실행 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)