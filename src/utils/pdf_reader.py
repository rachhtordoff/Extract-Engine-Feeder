import PyPDF2
from src import config


class PDFReader:
    def __init__(self):
        pass

    def read_pdf(self, filename):
        try:
            with open(filename, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                full_text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    full_text += page.extract_text() + "\n"
                return full_text
        except FileNotFoundError:
            print(f"File not found : {filename}")
            return None
        except PermissionError:
            print(f"No permission to read the file: {filename}")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
