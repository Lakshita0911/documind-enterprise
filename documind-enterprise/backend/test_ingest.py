import os
import sys
from backend.ingest import ingest_pdf

pdf_path = "uploads/sample.pdf"
if not os.path.exists(pdf_path):
    print(f"PDF not found: {pdf_path}")
    print("Please put your PDF in the uploads folder as sample.pdf or update test_ingest.py.")
    sys.exit(1)

chunk_count = ingest_pdf(pdf_path)
print(f"Total chunks stored: {chunk_count}")