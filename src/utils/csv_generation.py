import csv
import json
from datetime import datetime


def create_csv(data, doc_type):
    rows = []

    max_descriptions = max(len(descriptions) for descriptions in data.values())

    headers = set()

    for url, descriptions in data.items():
        for i, desc in enumerate(descriptions):
            row = {'url': url if i == 0 else '', 
                **{f"{key}_{i+1}": value for key, value in desc.items()}}
            headers.update(row.keys())
            rows.append(row)

    # Get the current date
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Create the filename
    filename = f"{config.doc_location}{doc_type}_webscrape_{current_date}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    return filename