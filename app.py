from flask import Flask, render_template, request
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def load_emotion_data():
    """Load emotion data from the CSV file and organize it for analysis."""
    data = defaultdict(list)
    with open('emotion_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name']
            emotion = row['Emotion']
            data[name].append(emotion)

    return data

def classify_stress_level(emotions):
    """Classify stress levels based on emotion counts."""
    negative_emotions = ['sad', 'angry', 'fearful']
    stress_count = sum(1 for emotion in emotions if emotion in negative_emotions)
    total_emotions = len(emotions)

    if stress_count / total_emotions > 0.5:
        return "Highly Stressed"
    elif stress_count / total_emotions > 0.2:
        return "Little Stress"
    else:
        return "No Stress"

def create_emotion_bar_graph(emotions, name):
    """Generate a bar graph of emotions for the selected user."""
    emotion_counts = defaultdict(int)
    for emotion in emotions:
        emotion_counts[emotion] += 1

    # Create the bar graph
    emotions_list = list(emotion_counts.keys())
    counts_list = list(emotion_counts.values())

    plt.figure(figsize=(10, 5))
    plt.bar(emotions_list, counts_list, color='skyblue')
    plt.title(f"Emotion Distribution for {name}")
    plt.xlabel("Emotion")
    plt.ylabel("Count")
    plt.tight_layout()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the image to display on the website
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_emotion_data()
    selected_name = None
    stress_level = None
    graph = None

    if request.method == 'POST':
        selected_name = request.form['name']
        if selected_name in data:
            emotions = data[selected_name]
            stress_level = classify_stress_level(emotions)
            graph = create_emotion_bar_graph(emotions, selected_name)

    return render_template('index.html', names=data.keys(), selected_name=selected_name, stress_level=stress_level, graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
