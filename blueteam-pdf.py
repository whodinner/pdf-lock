import os
from PyPDF2 import PdfReader

def blue_team_scan(folder="."):
    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found for scanning.")
        return

    for file in pdf_files:
        path = os.path.join(folder, file)
        reader = PdfReader(path)

        print(f"\nScanning: {file}")
        # Check encryption
        if reader.is_encrypted:
            print("  - PDF is encrypted (password protected).")
        else:
            print("  - PDF is not encrypted.")

        # Check for watermark text (naive scan of content)
        try:
            text = ""
            for page in reader.pages[:3]:  # only first 3 pages
                text += page.extract_text() or ""
            if "CONFIDENTIAL" in text.upper():
                print("  - Watermark 'CONFIDENTIAL' detected.")
            else:
                print("  - No obvious watermark text detected.")
        except:
            print("  - Could not extract text (possible image-based PDF).")

        # Check metadata
        metadata = reader.metadata
        if metadata:
            print("  - Metadata found:")
            for key, value in metadata.items():
                print(f"    {key}: {value}")
        else:
            print("  - No metadata present.")

if __name__ == "__main__":
    blue_team_scan(".")
