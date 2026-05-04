# Analyse-de-documents-comptables

A Python data pipeline designed to extract structured information from accounting documents in PDF format. The project uses direct text extraction and OCR (Optical Character Recognition) techniques to process various types of financial documents.

## 🚀 Features

*   **Automatic Extraction**: Identifies and automatically extracts data from PDF documents.
*   **Multiple Document Support**: Supports extraction from:
    *   Balance sheets (Bilans comptables)
    *   Income statements (Comptes de résultat)
    *   Invoices (Factures)
    *   Tax returns (Liasses fiscales)
*   **Dual Approach (Text & OCR)**: Uses `pdfplumber` to extract native text and `tesseract` as a fallback or for scanned documents (images).
*   **Two Execution Modes**:
    *   Command Line Interface (CLI)
    *   REST API (with FastAPI)
*   **Dockerized**: Ready to be deployed easily with its `Dockerfile`.

## 🏗️ Pipeline Architecture

The document processing follows a structured data flow to ensure optimal extraction, whether the PDF is native or scanned.

```text
PDF Input 
   │
   ▼
Text vs Image Detection (Content analysis)
   │
   ├─► If native text: Full text extraction (pdfplumber)
   │
   └─► If scanned: OCR Fallback (tesseract + pdf2image)
   │
   ▼
Fields Extraction & Structuring (Business rules + Regex)
   │
   ▼
JSON Output (Structured and typed data)
```

### Main Pipeline Functions
1. **PDF Type Detection** (`readers.pdf_type`): Analyzes whether the document contains selectable text or if it is a scan (image).
2. **Raw Extraction** (`readers.text_extractor`): Retrieves raw text and tables (using `pdfplumber`). If the text is non-existent or unreadable, OCR (`pytesseract`) takes over.
3. **Document Identification** (`field_extractors.commun`): Determines the nature of the document (invoice, balance sheet, etc.) by analyzing keywords in the raw text.
4. **Specific Extraction** (`field_extractors.*`): Applies Regular Expressions (Regex) and specific business rules based on the document type to isolate amounts, dates, SIRET, VAT, etc.

## 🛠️ Requirements

### System Dependencies
To use OCR, you must install certain system dependencies (these are included in the Docker image):
*   `tesseract-ocr`
*   `tesseract-ocr-fra` (for French language recognition)
*   `poppler-utils`

### Python Dependencies
The required Python packages are listed in `requirements.txt`:
*   `fastapi`
*   `uvicorn`
*   `pdfplumber`
*   `pytesseract`
*   `pdf2image`
*   `pillow`
*   `python-multipart`
*   `pytest`
*   `httpx`

## 📦 Installation

### Option 1: Local Usage (Virtualenv)

1. Clone the repository and navigate to the project folder:
   ```bash
   cd Analyse-de-documents-comptables
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
*(Make sure you have previously installed Tesseract and Poppler on your host system).*

### Option 2: Usage with Docker

This is the recommended method as it automatically installs all system dependencies.

1. Build the Docker image:
   ```bash
   docker build -t analyse-comptable-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 analyse-comptable-api
   ```

## 💻 Usage

### API Mode (FastAPI)

Run the API locally:
```bash
python src/main.py
```
The API will be available at `http://localhost:8000`. 

**Interactive Documentation (Swagger UI):**
Once the API is running, go to `http://localhost:8000/docs` to directly test the endpoints from your browser visually and interactively.

**Usage example with cURL:**
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample_pdfs/04_facture_atelier_mixte.pdf"
```

**JSON Response Example (200 OK):**
```json
{
  "file_name": "04_facture_atelier_mixte.pdf",
  "pdf_type": "mixed",
  "extracted_data": {
    "document_type": "facture",
    "company_name": "Atelier Boisé du Sud",
    "facture_number": "AB-2026-019",
    "limit_date": "05/04/2026",
    "SIRET": "512 709 004 00013",
    "tva_number": "FR 75 512709",
    "total_ht": "4 500,00€",
    "total_ttc": "5 400,00€",
    "tva": {
      "percentage": "20%",
      "amount": "900,00€"
    }
  }
}
```

### CLI Mode (Command Line)

You can process a file directly from the command line. The result will be exported in JSON format.

```bash
python src/main.py path/to/your/document.pdf
```
The result file will be saved with the same name (but with the `.json` extension) in the `output/` directory.

## ⚠️ Limitations

This project is robust but has some limitations related to its rule-based approach:
*   **Format Dependent**: Extraction by Regex is optimized for specific document formats. A major change in the layout of an invoice could cause certain rules to fail.
*   **Scan Quality**: OCR (`tesseract`) is less accurate on noisy, wrinkled scanned documents with low resolution or uneven lighting.
*   **No Machine Learning (ML)**: The current extraction does not use advanced Artificial Intelligence models to guess the context; it strictly relies on textual patterns and table positions.

## 🧪 Tests and Quality

To ensure the reliability of the API, a test suite has been implemented using `pytest` and `FastAPI's TestClient`. These tests verify that the `/upload` endpoint correctly handles valid PDF files, rejects invalid formats (like `.txt`), and returns the expected JSON data structures.

You can run the test suite using the following command:
```bash
python -m pytest tests/
```

## 📚 Documentation

The project includes automatically generated technical documentation using `pdoc`.

To view the documentation interactively in your browser, run:
```bash
pdoc src/
```

To export the documentation as static HTML files in a `docs/` directory:
```bash
pdoc -o docs/ src/
```

## 📁 Project Structure

*   `src/main.py`: Main entry point (Launches the API or the CLI).
*   `src/pipeline/`: API logic (`api.py`) and document routing (`router.py`).
*   `src/readers/`: Utilities for PDF reading and text/table extraction.
*   `src/field_extractors/`: Specific extraction logic for each document type (balance sheet, invoice, etc.).
*   `tests/`: Directory containing automated tests for the project.
*   `sample_pdfs/`: Test PDF documents.
*   `output/`: Directory containing JSON files exported in CLI mode.
*   `Dockerfile`: Containerized environment configuration.
*   `requirements.txt`: Python dependencies.
