from PyPDF2 import PdfReader

def read_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""

        # Extract text from each page
        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        doc_info = {
            "pages": len(reader.pages),
            "words": len(text.split()),
            "characters": len(text)
        }

        return text.strip(), doc_info

    except Exception:
        return None, None