from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile
from langchain.document_loaders import PyMuPDFLoader

router = APIRouter()


@router.post("/add")
def upload_file(file: UploadFile):
    with NamedTemporaryFile() as tmp:
        tmp.write(file.file.read())

        loader = PyMuPDFLoader(file_path=tmp.name)
        pages = loader.load(option="html")

    return {"filename": file.filename, "pages": len(pages)}
