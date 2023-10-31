import csv
import json
from datetime import datetime
from src import config
import pandas as pd

def create_csv(data, doc_type):
    rows = []
    headers = set([doc_type, 'info'])
    for extract in data:
        for key, value in extract.items():
            row_data = {doc_type: key, 'info': value}
            rows.append(row_data)

    # Get the current date
    current_date = datetime.now().strftime("%d-%m-%Y")
    # Create the filename
    new_doc_type = doc_type.replace(' ','_')
    filename = f"/opt/src/documents/{new_doc_type}_extract_{current_date}.csv"

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
            # Load CSV file into a pandas DataFrame
            df = pd.read_csv(filename)
            return df
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        except PermissionError:
            print(f"No permission to read the file: {filename}")
            return None
        except pd.errors.EmptyDataError:
            print(f"The file is empty: {filename}")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None