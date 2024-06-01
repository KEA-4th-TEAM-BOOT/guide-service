import os
import openai
from fastapi import APIRouter
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage
from core.clean import clean_html
from models.text import Text
from schemas.tag import TagResponse

load_dotenv()

router = APIRouter()

@router.post('/tag', response_model=TagResponse)
async def tag(text: Text):
    chatgpt = AzureChatOpenAI(deployment_name=os.getenv('DEPLOYMENT_NAME'),
                              temperature=1,
                              callbacks=[StreamingStdOutCallbackHandler()])

    messages = [
        SystemMessage(content='너는 입력 받은 글에서 적당한 해시태그를 추천해주는 가이드야. 키워드를 4개만 선정해서 ,로 구분해서 태그의 텍스트만 응답해줘.'),
        HumanMessage(content=clean_html(text.text))
    ]

    response = chatgpt(messages).content

    tags = [tag.strip() for tag in response.split(',')]

    return TagResponse(
        new_tag = tags
    )
