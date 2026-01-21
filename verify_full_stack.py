
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_project.settings')
django.setup()

print("--- System Verification ---")
print(f"Base Directory: {settings.BASE_DIR}")

# Check Tesseract
tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tess_path):
    print(f"[OK] Tesseract found at: {tess_path}")
else:
    print(f"[FAIL] Tesseract NOT found at: {tess_path}")

# Check Poppler
poppler_path_lib = os.path.join(settings.BASE_DIR, 'poppler', 'Library', 'bin')
poppler_path_bin = os.path.join(settings.BASE_DIR, 'poppler', 'bin')

if os.path.exists(poppler_path_lib):
    print(f"[OK] Poppler found at: {poppler_path_lib}")
elif os.path.exists(poppler_path_bin):
    print(f"[OK] Poppler found at: {poppler_path_bin}")
else:
    print(f"[FAIL] Poppler NOT found in project directory.")

# Test Import
try:
    from ai.resume_parser import extract_text_from_pdf
    print("[OK] resume_parser imported successfully.")
except Exception as e:
    print(f"[FAIL] Error importing resume_parser: {e}")

print("--- Verification Complete ---")
