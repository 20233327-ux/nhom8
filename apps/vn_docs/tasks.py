import os
from celery import shared_task
from django.conf import settings
from vn_docs.models import Document
import pytesseract
from PIL import Image
import pdfplumber

@shared_task
def process_document_ocr(doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
        file_path = doc.file_attachment.path
        ext = os.path.splitext(file_path)[1].lower()
        extracted_text = ""

        if ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff']:
            extracted_text = pytesseract.image_to_string(Image.open(file_path), lang='vie+eng')

        if extracted_text:
            doc.content_extracted = extracted_text
            doc.save()
            return f"OCR completed for {doc.doc_number}"
        return f"No text extracted for {doc.doc_number}"
    except Exception as e:
        return f"Error OCR: {str(e)}"
