import os
import openai
from fastapi import APIRouter
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from models.text import Text
from schemas.spelling import SpellingResponse

load_dotenv()

router = APIRouter()

@router.post('/spelling', response_model=SpellingResponse)
async def spelling(text: Text):
    chatgpt = AzureChatOpenAI(deployment_name=os.getenv('DEPLOYMENT_NAME'),
                              temperature=1,
                              callbacks=[StreamingStdOutCallbackHandler()])

    messages = [
        SystemMessage(content='너는 입력 받은 글의 틀린 맞춤법을 수정을 도와주는 가이드야.'),
        HumanMessage(content=text.text)
    ]

    response = chatgpt(messages)

    return SpellingResponse(
        original_text=text,
        new_text=Text(text=response.content)
    )
