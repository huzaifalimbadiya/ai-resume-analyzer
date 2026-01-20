
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from ai.resume_parser import extract_text_from_pdf
    print("Successfully imported extract_text_from_pdf")
except Exception as e:
    print(f"Failed to import: {e}")
    sys.exit(1)

# Test with non-existent file
text, error = extract_text_from_pdf("non_existent_file.pdf")
print(f"Result for non-existent file: Text='{text}', Error='{error}'")

if error == "File not found.":
    print("Test passed: Handled non-existent file correctly.")
else:
    print("Test failed: Unexpected error message.")

