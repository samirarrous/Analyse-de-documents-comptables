from fastapi.testclient import TestClient
from src.pipeline.api import app
import src.pipeline.api as api  # noqa: F401, F811, F841
# Creating test client
client = TestClient(app)

""" testing an invalid file"""

def test_upload_invalid_file_type():
    # fake text file with wrong format
    files = {"file": ("test.txt", b"Ceci n'est pas un pdf", "text/plain")}
    response = client.post("/upload", files=files)
    
    # should return error 
    assert response.status_code == 400
    assert response.json() == {"detail": "File must be pdf"}

""" testing a valid pdf file"""

def test_upload_valid_pdf(monkeypatch):
    # creating fake function
    def mock_route_document(file_path):
        return {
            "pdf_type": "mixed",
            "extracted_data": {
                "document_type": "facture",
                "company_name": "Formalis",
                "total_ht": "100.00"
            }
        }
    
    # injecting the function
    monkeypatch.setattr(api.router, "route_document", mock_route_document)
    
    # sending a test  pdf file
    minimal_pdf = b"%PDF-1.4\n%EOF\n"
    files = {"file": ("test.pdf", minimal_pdf, "application/pdf")}
    response = client.post("/upload", files=files)
    
    # verifying the response
    assert response.status_code == 200
    
    # verifying the json
    data = response.json()
    assert data["pdf_type"] == "mixed" 
    assert data["extracted_data"]["document_type"] == "facture"
    assert data["extracted_data"]["company_name"] == "Formalis"