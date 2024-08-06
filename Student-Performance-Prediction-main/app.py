from flask import Flask, request, render_template
import pickle
# Importing models
model = pickle.load(open('StudentPerformancePrediction.pkl', 'rb'))
model1 = pickle.load(open('CRT_Model.pkl', 'rb'))

# Creating Flask app
app = Flask(__name__)

def get_message(result):
    if result >= 90:
        return "Excellent performance!"
    elif 80 <= result < 90:
        return "Good performance!"
    elif 70 <= result < 80:
        return "Fair performance. "
    else:
        return "Work hard to improve your performance."

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/crt')
def index2():
    return render_template("index2.html")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Retrieve form data
        if 'Xth_CGPA' in request.form:
            Xth_CGPA = float(request.form['Xth_CGPA'])
            Intermediate_CGPA = float(request.form['Intermediate_CGPA'])
            First_Semester_CGPA = float(request.form['First_Semester_CGPA'])
            Second_Semester_CGPA = float(request.form['Second_Semester_CGPA'])
            Third_Semester_CGPA = float(request.form['Third_Semester_CGPA'])
            Fourth_Semester_CGPA = float(request.form['Fourth_Semester_CGPA'])
            Fifth_Semester_CGPA = float(request.form['Fifth_Semester_CGPA'])
            Clubs_Participation = float(request.form['Clubs_Participation'])
            Leadership = float(request.form['Leadership'])
            More_than_3_Programming_Lang = float(request.form['More_than_3_Programming_Lang'])
            Laboratory_Skills = float(request.form['Laboratory_Skills'])

            # Perform prediction
            feature_list = [Xth_CGPA, Intermediate_CGPA, First_Semester_CGPA, Second_Semester_CGPA,
                            Third_Semester_CGPA, Fourth_Semester_CGPA, Fifth_Semester_CGPA,
                            Clubs_Participation, Leadership, More_than_3_Programming_Lang, Laboratory_Skills]

            prediction = model.predict([feature_list])
        
            # Process prediction result
            if prediction[0]:
                result = "{:.2f} %".format(prediction[0])
                message = get_message(prediction[0])
            else:
                result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
                message = "Error: {}".format(result)
    except Exception as e:
        result = "Error processing the prediction: {}".format(str(e))
        message = "Error: {}".format(result)

    return render_template('index.html', result=result, message=message)

@app.route("/predict_crt", methods=['POST'])
def predict_crt():
    try:
        # Retrieve form data
        if 'CGPA' in request.form:
            CGPA = float(request.form['CGPA'])
            Logical_Reasoning = float(request.form['Logical_Reasoning'])
            Problem_Solving_Thinking = float(request.form['Problem_Solving_Thinking'])
            Oral_Assessments = float(request.form['Oral_Assessments'])
            Team_Experience = float(request.form['Team_Experience'])
            Time_Management = float(request.form['Time_Management'])
            Internship = float(request.form['Internship'])

            # Perform prediction
            feature_list = [CGPA, Logical_Reasoning, Problem_Solving_Thinking, Oral_Assessments,
                            Team_Experience, Time_Management, Internship]

            prediction = model1.predict([feature_list])
        
            # Process prediction result
            if prediction[0]:
                result1 = "{:.2f} %".format(prediction[0])
                message1 = get_message(prediction[0])
            else:
                result1 = "Sorry, we could not determine the best crop to be cultivated with the provided data."
                message1 = "Error: {}".format(result1)
    except Exception as e:
        result1 = "Error processing the prediction: {}".format(str(e))
        message1 = "Error: {}".format(result1)

    return render_template('index2.html', result=result1, message=message1)

# Python main
if __name__ == "__main__":
    app.run(debug=True)

