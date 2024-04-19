import openai
from fastapi import APIRouter
from langchain.chat_models import AzureChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from models.text import Text
from schemas.tag import TagResponse

router = APIRouter()

@router.post('/tag', response_model=TagResponse)
async def tag(text: Text):
    chatgpt = AzureChatOpenAI(deployment_name='boot-35',
                              temperature=1,
                              callbacks=[StreamingStdOutCallbackHandler()])

    messages = [
        SystemMessage(content='너는 입력 받은 글에서 적당한 해시태그를 추천해주는 가이드야.'),
        HumanMessage(content=text)
    ]

    return chatgpt(messages)
