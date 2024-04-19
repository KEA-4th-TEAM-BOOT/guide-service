import openai
from fastapi import APIRouter
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from models.text import Text
from schemas.spelling import SpellingResponse

router = APIRouter()

@router.post('/spelling', response_model=SpellingResponse)
async def spelling(text: Text):
    chatgpt = AzureChatOpenAI(deployment_name='boot-35',
                              temperature=1,
                              callbacks=[StreamingStdOutCallbackHandler()])

    messages = [
        SystemMessage(content='너는 입력 받은 글의 틀린 맞춤법을 수정을 도와주는 가이드야.'),
        HumanMessage(content=text)
    ]

    return chatgpt(messages)
