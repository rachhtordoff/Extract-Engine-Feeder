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

    # Create the filename
    filename = f"{config.doc_location}{doc_type}_webscrape_{current_date}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    return filename
