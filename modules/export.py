import csv
import os

def export_csv(filename, data):
    # Create the CSV file and write the headers if they don't exist
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Policy Name', 'Policy ID', 'Policy Status', 'Policy Severity', 'Policy Labels'])

    # Append the data to the CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)