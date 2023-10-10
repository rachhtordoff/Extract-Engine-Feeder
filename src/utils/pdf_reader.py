import pdfplumber
from src import config


class PDFReader:
    def __init__(self):
        pass

    def read_pdf(self, filename):
        try:
            with pdfplumber.open(f"{config.doc_location}{filename}") as pdf:
                # Concatenating text contents of all pages into a single string.
                full_text = "\n".join([page.extract_text() for page in pdf.pages])
                return full_text
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        except PermissionError:
            print(f"No permission to read the file: {filename}")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
