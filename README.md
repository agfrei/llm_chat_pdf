# llm_chat_pdf
This project uses [LangChain](https://www.langchain.com/), [OpenAI GPT](https://openai.com/product) and [chroma](https://www.trychroma.com/) to index your PDF files and then let you chat with them.

## Running locally
You should install [PDM](https://pdm.fming.dev/latest/) and then `pdm install` on both `api` and `frontend` folders.

Inside `api` folder you should have a `.env` file with the following variables (or you can have them on your system, as you prefer)
- `OPENAI_API_KEY`: Your API key for OpenAI API.
- `CHROMA_PERSIST_DIRECTORY`: Local folder where embeddings will be stored.

Inside `frontend` folder you should have a `.env` file with the following variables (or you can have them on your system, as you prefer)
- `API_URL`=localhost
- `API_PORT`=8000
- `CHATBOT_PORT`=8001

Then, open a terminal window, navigate to `api` folder and run:
```shell
pdm run api
```
This will start your API and put it running on port `8000`.

To start the chatbot UI is similar, you just need to navigate to `frontend` folder and run:
```shell
pdm run chatbot
```
This will start the chatbot UI on port `8001`, so you can navigate on your browser to `localhost:8001` and start talking.

Remember to upload some documents before ask questions. Have fun!!!

## Possible improvements or modifications

Feel free to do some improvements or modifications, for example you can try:
- Add support for other document types
- Change the vectordb
- Change the LLM, you can try an open source like Llama or any other.
- Use some metadata on the retrieval. Or even change teh retrieval strategy
- Change document splitting strategy.
- Improve document loading removing unecessary repetitive parts like header and footer.

## Splitting Strategy
To create a more semantic chunks, we developed the following strategy:

1. Load PDF as HTML using [PyMuPDF](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#using-pymupdf)

2. Split each `div` and `span` into `sections` with font-size as metadata (similar as described [here](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#using-pdfminer-to-generate-html-text))

3. Convert into markdow using font size to infer headers (bigger fonts = top headers, lowest font = simple text). This is a very naive approach and can be improved, but for well structured documents with simple formatting should work pretty well.

4. Use [MarkdownHeaderTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/markdown_header_metadata) to split markdown into meanigful chunks.

5. Use [RecursiveCharacterTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter) to split in even small chunks, in the case the previous splitter has ended with larger chunks.


### Strategy Limitations
As mentioned, this is a naive approach that assumes:
- Document is wel organized into sessions.
- It follows a meaningful structure of headers and subheaders.
- Larger fonts = Top headers

#### Possible failure scenarios
If you have a document which below of each subheader you have a enphasys text with a font size smaller than the "normal" font size for the document, this font will be assumed as the "normal" and the real "normal" will be evaluated as some level of header.

Other scenario is when your doc has some quotations between the text, imagine these quotations has bigger fonts than some headers, in this case they will be interpreted as a header.
