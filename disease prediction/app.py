from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Function to load the dataset from the CSV file
def load_disease_data(file_path="data/dataset.csv"):
    disease_data = {}
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            disease = row["Disease"]
            symptoms = row["Symptoms"].split(",")
            disease_data[disease] = [symptom.strip().lower() for symptom in symptoms]
    return disease_data

# Function to predict the disease based on user input symptoms
def predict_disease(input_symptoms, disease_data):
    input_symptoms_set = set(input_symptoms.lower().split(","))
    max_match_count = 0
    predicted_disease = "Unknown"

    for disease, symptoms in disease_data.items():
        symptoms_set = set(symptoms)
        match_count = len(input_symptoms_set.intersection(symptoms_set))

        if match_count > max_match_count:
            max_match_count = match_count
            predicted_disease = disease

    return predicted_disease

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Load the disease data once the user submits symptoms
    disease_data = load_disease_data()
    
    symptoms = request.form["symptoms"]
    prediction = predict_disease(symptoms, disease_data)
    
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
