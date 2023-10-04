from pydantic import BaseModel


class ChatMessage(BaseModel):
    question: str
    answer: str


class Chat(BaseModel):
    question: str
    history: list[ChatMessage] = []
