from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):
    if pdf_file is not None:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    return None