from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from src.app.chat import schemas
from src.app.core.settings import Settings


class Chat:
    def __init__(self, settings: Settings):
        embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        vectordb = Chroma(
            persist_directory=settings.chroma_persist_directory,
            embedding_function=embeddings,
        )

        self._retriever = vectordb.as_retriever()

        self._llm = ChatOpenAI(
            model_name=settings.openai_model_name,
            temperature=0,
            openai_api_key=settings.openai_api_key,
        )

    def get_answer(self, message: schemas.Chat):
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self._llm,
            chain_type="stuff",
            retriever=self._retriever,
            return_source_documents=True,
            return_generated_question=True,
            # chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )  # TODO: remove hardcoded

        history = [(qa.question, qa.answer) for qa in message.history]
        res = qa_chain({"question": message.question, "chat_history": history})

        return res
