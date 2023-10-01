import gradio as gr
import requests


def upload_file(file):
    with open(file.name, "rb") as f:
        res = requests.post(
            "http://localhost:8000/file/add",
            files={"file": (file.name, f.read())},
        )
        print(res)
        print(res.json())
    return


with gr.Blocks() as app:
    file = gr.File()
    upload_btn = gr.Button("Upload")
    upload_btn.click(upload_file, file)

if __name__ == "__main__":
    gr.close_all()
    app.launch(share=False, server_port=8001)
