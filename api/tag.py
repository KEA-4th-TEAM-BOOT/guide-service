import os
import openai
from fastapi import APIRouter
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage
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
        SystemMessage(content='너는 입력 받은 글에서 적당한 해시태그를 추천해주는 가이드야.'),
        HumanMessage(content=text.text)
    ]

    response = chatgpt(messages).content

    return TagResponse(
        original_text=text,
        new_tag=Text(text=response)
    )
