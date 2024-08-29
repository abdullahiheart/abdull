from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load(r'C:\Users\abdal\Music\Student Recomendation\rf_model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        
        # Collect features (marks for all subjects) from the form
        features = [
            float(data.get('Tarbiyo', 0)),
            float(data.get('Arabi', 0)),
            float(data.get('Biology', 0)),
            float(data.get('Chemistry', 0)),
            float(data.get('Physics', 0)),
            float(data.get('Math', 0)),
            float(data.get('History', 0)),
            float(data.get('Geography', 0)),
            float(data.get('Somali', 0)),
            float(data.get('Business', 0)),
            float(data.get('Technology', 0))
        ]
        
        # Get the subject names and their corresponding marks
        subject_marks = {subject: float(data.get(subject, 0)) for subject in [
            'Tarbiyo', 'Arabi', 'Biology', 'Chemistry', 'Physics',
            'Math', 'History', 'Geography', 'Somali', 'Business', 'Technology'
        ]}
        
        # Predict the recommended field
        prediction = model.predict([features])[0]
        
        # Render the result template with the prediction and subject marks
        return render_template('result.html', recommended_field=prediction, subject_marks=subject_marks)
    except Exception as e:
        return jsonify({'error': str(e), 'recommended_field': 'Error processing request'})

if __name__ == '__main__':
    app.run(debug=True)
