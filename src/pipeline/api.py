"""
FastAPI application definition and endpoints for the document analyzer.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
import tempfile
import os
from . import router

app = FastAPI()

@app.get("/")
def root():
    """Redirects the root URL to the interactive API documentation."""
    return RedirectResponse(url="/docs")

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    API endpoint to upload and process a PDF accounting document.

    Args:
        file (UploadFile): The PDF file uploaded via multipart/form-data.

    Raises:
        HTTPException: If the uploaded file is not a PDF (400 Bad Request).

    Returns:
        dict: A JSON response containing the extracted structured data and the file name.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be pdf")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = router.route_document(tmp_path)
        # tried to add this in router.py but it gave a wrong file name 
        final = {
            "file_name": file.filename,  #putting filename in the beginning
            **result
        }
        return final
    finally:
        os.unlink(tmp_path)  