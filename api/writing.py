import openai
from fastapi import APIRouter
from models.guide import Guide
from schemas.writing import WritingResponse

router = APIRouter()

@router.post('/writing', response_model=WritingResponse)
async def writing(guide: Guide):
    result = openai.chat.completions.create(
        model='dev-gpt-35-turbo',
        temperature=1,
        messages=[
            {'role': 'system', 'content': '너는 사용자들이 포스트를 잘 작성할 수 있도록 도와주는 가이드야.'},
            {'role': 'user', 'content': '주제는 ' + guide.subject},
            {'role': 'user', 'content': '글의 길이는 ' + guide.length}
        ]
    )

    return result.choices[0].message.content