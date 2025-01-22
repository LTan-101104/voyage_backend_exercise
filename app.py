from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional, List
from PyPDF2 import PdfReader
from helper import process_parsed_data
from extractor_core.main import parse_text
import io
from datetime import datetime

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "main_db"
COLLECTION_NAME = "resume"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


app = FastAPI()
class ResponseMessage(BaseModel):
    message : Optional[str] = Field(None, example = "sample message")

class Data(BaseModel):
    introduction : dict[str, str] = Field(..., example={
        "first_name": "User Name",
        "last_name": "User Last Name",
        "title": "user Title",
        "tagline": "Prudent Software Engineer."
    },)
    contact : dict[str, str] = Field(..., example = {
        "email": "abc@woyage.ai",
        "phone": "1111111111",
        "address_line": "abc Dr",
        "address_city": "San Franciso",
        "address_state": "CA",
        "address_zipcode": "00000",
        "address_country": "United States",
        "linkedin": "linkedin.com/user-111"
    })
    summary : dict[str, str] = Field(..., example = {
        "description": "Highly motivated ....."
    })

#for responding to /resume/parse route
class ResponseData(ResponseMessage):
    result : str = Field(..., example = 'success')
    data : Optional[Data] = Field(None)

class ObjectTime(BaseModel):
    date : datetime = Field(..., example = datetime.now())

#for storing and retrieving data
class StoreData(BaseModel):
    id : str = Field(..., alias='_id', example = "6777c77b4e437abb2fb9850a")
    content : Data = Field(...)
    created_at : datetime = Field(...)
    updated_at : datetime = Field(...)


def item_serializer(item):
    item['_id'] = str(item['_id'])
    return item

def attach_time(obj, is_update = False):
    if not is_update:
        obj['created_at'] = datetime.now()
        obj['updated_at'] = datetime.now()
    else:
        obj['updated_at'] = datetime.now()

# def retrieve_content(contents, file_type) -> str:
#     # Read file contents
#     text = ""
#     # Process file based on content type
#     if file_type == "application/pdf":
#         # Read PDF content
#         pdf_reader = PdfReader(io.BytesIO(contents))
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#         # Read DOCX content
#         doc = docx.Document(io.BytesIO(contents))
#         text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
#     print("DEBUG")
#     print(text)
#     return text


@app.get('/test', response_model = ResponseMessage)
def response_test():
    return {"message" : "Successfully returned"}

@app.post("/resume/parse", response_model=ResponseData)
async def get_file(file : UploadFile = File(...)): #! require file
    if file.content_type not in {"application/pdf"}:
        raise HTTPException(status_code=400, detail="Only accept pdf file")
    try:
        contents = await file.read()
        text = ""
        pdf_reader = PdfReader(io.BytesIO(contents))
        for page in pdf_reader.pages:
            text += page.extract_text()
        parsed = parse_text(text)
        data = process_parsed_data(parsed)
        #!store in database
        store_obj = {"content" : data}
        attach_time(store_obj)
        await collection.insert_one(store_obj)
        return{
            'result' : 'success',
            "message": "Resume parsed.",
            "data" : data
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail = f"Error at get_file(): {e}")
    
#!testing route for database
@app.get('/resume/parse', response_model = List[Optional[StoreData]])
async def get_all():
    try:
        data = await collection.find().to_list(100)
        print(data)
        return [item_serializer(item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error at get_all() : {e}")