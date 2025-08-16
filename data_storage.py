#2.data_storage.py
import csv
import os

# Path to store emotion data
data_file = 'emotion_data.csv'

# Create or append to the CSV file
if not os.path.exists(data_file):
    with open(data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Timestamp', 'Emotion'])

def store_emotion_data(name, emotion, timestamp):
    """Store emotion data in a CSV file."""
    with open(data_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, timestamp, emotion])

