from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from src.app.core.settings import SettingsDep
from src.app.document.document import Document

router = APIRouter()


@router.post("/add")
def upload(file: UploadFile, settings: SettingsDep):
    with NamedTemporaryFile() as tmp:
        tmp.write(file.file.read())

        doc = Document(tmp.name, settings)
        doc.load()

    return {
        "filename": file.filename,
        "chunks": len(doc.chunks),
    }
