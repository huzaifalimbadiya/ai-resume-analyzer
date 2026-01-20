
import os
import sys

# Print current working directory
print(f"Current Working Directory: {os.getcwd()}")

# Define the paths as they are in the parser
possible_poppler_paths = [
    os.path.join(os.getcwd(), 'poppler', 'Library', 'bin'),
    os.path.join(os.getcwd(), 'poppler', 'bin'),
    os.path.join(os.getcwd(), '..', 'poppler', 'Library', 'bin'),
    os.path.join(os.getcwd(), '..', 'poppler', 'bin'),
]

found = False
for path in possible_poppler_paths:
    exists = os.path.exists(path)
    print(f"Checking path: {path} - Exists: {exists}")
    if exists:
        try:
            contents = os.listdir(path)
            has_tool = 'pdftoppm.exe' in contents or 'pdftoppm' in contents
            print(f"  Contains pdftoppm.exe: {has_tool}")
            if has_tool:
                print(f"  -> MATCH FOUND!")
                found = True
        except Exception as e:
            print(f"  Error listing dir: {e}")

if not found:
    print("Poppler NOT found in any checked paths.")
else:
    print("Poppler verification SUCCESS.")
