import csv
import json
from datetime import datetime
from src import config

def create_csv(data, doc_type):
    rows = []
    headers = set(['url'])
    
    for url, chunks in data.items():
        for chunk_name, contents in chunks.items():
            row_data = {'url': url}

            for key, val in contents.items():
                if isinstance(val, dict):
                    for sub_key, sub_val in val.items():
                        new_key = f"{key}_{sub_key}".replace(" ", "_").lower()
                        row_data[new_key] = sub_val
                        headers.add(new_key)
                else:
                    new_key = key.replace(" ", "_").lower() 
                    row_data[new_key] = val
                    headers.add(new_key)
            
            rows.append(row_data)

    # Get the current date
    current_date = datetime.now().strftime("%d-%m-%Y")
    print('doc_type')
    # Create the filename
    filename = f"{config.doc_location}{doc_type}_extract_{current_date}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    return filename

class CSVReader:
    def __init__(self):
        pass

    def read_csv(self, filename):
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
