import json
import os

import gradio as gr
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "localhost")
API_PORT = os.getenv("API_URL", "8000")
CHATBOT_PORT = os.getenv("API_URL", "8001")


def format_chat_history(chat_history):
    if chat_history:
        return [
            {"question": turn[0], "answer": turn[1]} for turn in chat_history
        ]
    return []


def respond(message, chat_history):
    formatted_history = format_chat_history(chat_history)

    url = f"{API_URL}:{API_PORT}"
    path = "chat/"
    body = {"question": message, "history": formatted_history}
    headers = {"Content-Type": "application/json"}

    res = requests.post(
        f"http://{url}/{path}", data=json.dumps(body), headers=headers
    )

    docs = ""
    question = ""
    if res.status_code == 200:
        res = res.json()
        chat_history.append((message, res["answer"]))
        docs = res["source_documents"]
        question = res["generated_question"]

    return "", chat_history, docs, question


def upload_file(file):
    with open(file.name, "rb") as f:
        url = f"{API_URL}:{API_PORT}"
        path = "add/"
        return_msg = ""

        res = requests.post(
            f"http://{url}/{path}",
            files={"file": (file.name, f.read())},
        )

        if res.status_code == 200:
            res = res.json()
            return_msg = (
                f"Uploaded file: {res['filename']}\nChunks: {res['chunks']}"
            )
    return return_msg


with gr.Blocks() as app:
    with gr.Tab("Chat"):
        with gr.Row():
            with gr.Column():
                chat_history = gr.Chatbot(height=240)
                msg = gr.Textbox(label="Message")
                btn = gr.Button("Send")
                clear = gr.ClearButton(
                    components=[msg, chat_history], value="Clear"
                )

            with gr.Column():
                with gr.Accordion("Details"):
                    question = gr.Textbox(label="Question sent to llm")
                    docs = gr.JSON(label="Returned docs from vector db")

        with gr.Row():
            with gr.Column():
                btn.click(
                    respond,
                    inputs=[msg, chat_history],
                    outputs=[msg, chat_history, docs, question],
                )
                msg.submit(
                    respond,
                    inputs=[msg, chat_history],
                    outputs=[msg, chat_history, docs, question],
                )

    with gr.Tab("Documents"):
        with gr.Row():
            with gr.Column():
                file = gr.File()
                upload_btn = gr.Button("Upload")
            with gr.Column():
                doc_info = gr.Textbox(lines=3)

        upload_btn.click(upload_file, file, doc_info)


if __name__ == "__main__":
    gr.close_all()
    app.launch(share=False, server_port=int(CHATBOT_PORT))
