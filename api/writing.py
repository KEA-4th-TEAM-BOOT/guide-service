import os
import openai
from fastapi import APIRouter
from dotenv import load_dotenv
from models.guide import Guide
from models.text import Text
from schemas.writing import WritingResponse

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_version = os.getenv('OPENAI_API_VERSION')

router = APIRouter()

@router.post('/writing', response_model=Text)
async def writing(guide: Guide):
    result = openai.chat.completions.create(
        model=os.getenv('DEPLOYMENT_NAME'),
        temperature=1,
        messages=[
            {'role': 'system', 'content': '너는 사용자들이 포스트를 잘 작성할 수 있도록 도와주는 가이드야.'},
            {'role': 'user', 'content': '글의 주제는 ' + guide.subject},
            {'role': 'user', 'content': '글의 대상 독자층은 ' + guide.reader},
            {'role': 'user', 'content': '글의 길이는 ' + guide.length},
            {'role': 'user', 'content': '글 제목의 스타일은 ' + guide.style}
        ]
    )

    response = result.choices[0].message.content

    #return WritingResponse(
    #    original_guide=guide,
    #    new_text=Text(text=response)
    #)
    return Text(text=response)