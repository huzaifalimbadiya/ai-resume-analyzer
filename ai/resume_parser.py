import pdfplumber
import os
import traceback
import PyPDF2
import pytesseract
from pdf2image import convert_from_path, exceptions as pdf2image_exceptions
import sys
from django.conf import settings

# Set Tesseract path if it's in a standard location (Windows)
POSSIBLE_TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    os.path.join(settings.BASE_DIR, 'tesseract', 'tesseract.exe'),
    os.getenv('TESSERACT_CMD')
]

for path in POSSIBLE_TESSERACT_PATHS:
    if path and os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

# Check for local Poppler (for pdf2image)
POPPLER_PATH = None
possible_poppler_paths = [
    os.path.join(settings.BASE_DIR, 'poppler', 'Library', 'bin'),
    os.path.join(settings.BASE_DIR, 'poppler', 'bin'),
]

for path in possible_poppler_paths:
    if os.path.exists(path) and ('pdftoppm.exe' in os.listdir(path) or 'pdftoppm' in os.listdir(path)):
        POPPLER_PATH = path
        print(f"Found Poppler at: {POPPLER_PATH}")
        break

if POPPLER_PATH and POPPLER_PATH not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + POPPLER_PATH

def extract_text_from_pdf(pdf_path):
    """
    Extracts full text from a PDF file.
    Tries pdfplumber -> PyPDF2 -> OCR (pytesseract).
    
    Returns:
        tuple: (extracted_text, error_message)
        - extracted_text: The text found (str)
        - error_message: None if successful, or a string explaining why it failed.
    """
    text = ""
    error_details = []
    
    print(f"Attempting to extract text from: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        return "", "File not found."

    # --- Method 1: pdfplumber ---
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                error_details.append("pdfplumber: PDF has no pages.")
            else:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
    except Exception as e:
        error_details.append(f"pdfplumber failed: {str(e)}")

    # --- Method 2: PyPDF2 (Fallback) ---
    # Only try if pdfplumber returned empty or whitespace-only text
    if not text.strip():
        print("pdfplumber yielded no text. Trying PyPDF2...")
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "" # Reset text
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            error_details.append(f"PyPDF2 failed: {str(e)}")

    # Check if we have valid text now
    if text.strip():
        return text.strip(), None

    # --- Method 3: OCR (Fallback for Scanned PDFs) ---
    print("Standard extraction failed. Attempting OCR...")
    try:
        # pdf2image requires Poppler
        # We explicitly pass the poppler_path if we found it locally
        if POPPLER_PATH:
            images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        else:
            images = convert_from_path(pdf_path)
        
        ocr_text = ""
        for i, image in enumerate(images):
            print(f"OCR processing page {i+1}...")
            # pytesseract requires Tesseract-OCR
            # This will raise TesseractNotFoundError if Tesseract is missing
            page_text = pytesseract.image_to_string(image)
            ocr_text += page_text + "\n"
        
        if ocr_text.strip():
            return ocr_text.strip(), None
        else:
            return "", "OCR completed but found no text (image might be too blurry or blank)."
            
    except pdf2image_exceptions.PDFInfoNotInstalledError:
        msg = f"OCR Failed: Poppler is not installed or not in PATH. (Checked path: {POPPLER_PATH if POPPLER_PATH else 'System PATH'})"
        print(msg)
        return "", msg
    except pytesseract.TesseractNotFoundError:
        msg = "OCR Failed: Tesseract-OCR is not installed or not in PATH. Please install Tesseract."
        print(msg)
        return "", msg
    except Exception as e:
        msg = f"Could not extract text. OCR failed: {str(e)}"
        print(msg)
        return "", msg
