from src.main import run_cli

""" testing an invalid pdf file"""

def test_cli_invalid_file(capsys):
    # test with non-existent file
    run_cli("non_existent_file.pdf")
    captured = capsys.readouterr()
    assert "file not found" in captured.out


""" testing a valid pdf file"""

def test_cli_valid_file(monkeypatch, tmp_path, capsys):
    # create a test file
    dummy_pdf = tmp_path / "test.pdf"
    dummy_pdf.write_text("%PDF-1.4\n")
    
    # mock router to prevent actual OCR execution
    def mock_route_document(file_path): 
        return {
            "pdf_type": "text",
            "extracted_data": {
                "document_type": "facture",
                "company_name": "Formalis"
            }
        }
        
    import src.main as main_module  # noqa: F401, F811, F841
    monkeypatch.setattr(main_module.router, "route_document", mock_route_document)
    
    # mock the JSON export so we don't write actual files
    def mock_export_to_json(result, filename):
        return f"output/{filename}"
        
    monkeypatch.setattr(main_module, "export_to_json", mock_export_to_json)
    
    # run the CLI command
    run_cli(str(dummy_pdf))
    # verify the success message
    captured = capsys.readouterr()
    assert "result exported : output/test.json" in captured.out