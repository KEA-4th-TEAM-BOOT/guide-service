import os
import openai
from fastapi import APIRouter
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage
from core.clean import clean_html
from models.text import Text
from schemas.spelling import SpellingResponse

load_dotenv()

router = APIRouter()

@router.post('/spelling', response_model=Text)
async def spelling(text: Text):
    chatgpt = AzureChatOpenAI(deployment_name=os.getenv('DEPLOYMENT_NAME'),
                              temperature=1,
                              callbacks=[StreamingStdOutCallbackHandler()])

    messages = [
        SystemMessage(content='너는 입력 받은 글의 틀린 맞춤법을 수정을 도와주는 가이드야. 맞춤법을 수정한 게시물을 응답해줘.'),
        HumanMessage(content=clean_html(text.text))
    ]

    response = chatgpt(messages).content

    #return SpellingResponse(
    #    original_text=text,
    #    new_text=Text(text=response)
    #)

    return Text(text=response)
