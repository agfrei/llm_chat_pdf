from fastapi import APIRouter

from src.app.chat import schemas
from src.app.chat.chat import Chat
from src.app.core.settings import SettingsDep

router = APIRouter()


@router.post("/")
def chat(message: schemas.Chat, settings: SettingsDep):
    chat = Chat(settings)
    answer = chat.get_answer(message)
    return answer
