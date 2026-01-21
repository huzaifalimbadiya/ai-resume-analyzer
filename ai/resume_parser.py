import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF using pdfplumber only.
    Render / Linux compatible. No OCR.
    """
    if not os.path.exists(pdf_path):
        return "", "File not found"

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text.strip():
            return text.strip(), None
        else:
            return "", "No readable text found in PDF (maybe scanned image)."

    except Exception as e:
        return "", str(e)
