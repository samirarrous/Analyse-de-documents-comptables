from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os
from . import router

app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be pdf")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = router.route_document(tmp_path)
        final = {
            "file_name": file.filename,
            "pdf_type": result.pop("pdf_type", "unknown"),
            **result
        }
        return final
    finally:
        os.unlink(tmp_path)  