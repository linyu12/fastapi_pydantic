# pydantic
from instructor import openai_schema
from pydantic import Field, BaseModel

# Path: fastapi_pydabtic.py
from fastapi import FastAPI
# pip install fastapi uvicorn
# pip install fastapi==0.78.8
# pip install uvicorn==0.17.6
# uvicorn fastapi_pydantic:app --reload
# http://localhost:8000/docs#/

import openai
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

app = FastAPI()
'''app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)'''

@openai_schema
class CommodityPrice(BaseModel):
    name: str = Field(..., description="commodity's full name") #于数据模型的定义，用来指定字段的数据类型、验证规则和描述，以便生成文档或执行数据验证。
    print: int

def ai_response(msg):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            functions=[CommodityPrice.openai_schema],
            function_call={"name": CommodityPrice.openai_schema["name"]},
            messages=[
                {"role": "system", "content": "Extract user details from my requests"},
                {"role": "user", "content": msg},
            ],
        )
        Commodity_details =CommodityPrice.from_response(completion)
        return Commodity_details
    except Exception as e:
        return {"error": str(e)}

#while True: 
@app.post("/items/")
def create_item(msg):
    return ai_response(msg)
    
