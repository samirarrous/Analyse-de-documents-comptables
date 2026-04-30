import pdfplumber



def define_type(file_path):
    has_text = False
    has_image = False

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.extract_text() :
                has_text = True
            if page.images:  
                has_image = True

    if has_text :
        if has_image:
            return "mixed"
        return "native"
    else:
        return "scan"            
        