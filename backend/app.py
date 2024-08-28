from flask import Flask, request, jsonify
from flask_cors import CORS
from objective import ObjectiveTest
from subjective import SubjectiveTest

app = Flask(__name__)
CORS(app) 

app.secret_key = 'aica2'

@app.route('/')
def index():
    return "Welcome to the test generator API"

@app.route('/test_generate', methods=["POST"])
def test_generate():
    if request.method == "POST":
        data = request.json  
        inputText = data.get("itext")
        testType = data.get("test_type")
        noOfQues = int(data.get("noq"))

        if testType == "objective":
            objective_generator = ObjectiveTest(inputText, noOfQues)
            question_list, answer_list = objective_generator.generate_test()
            testgenerate = list(zip(question_list, answer_list))
            return jsonify({'cresults': testgenerate})
        elif testType == "subjective":
            subjective_generator = SubjectiveTest(inputText, noOfQues)
            question_list, answer_list = subjective_generator.generate_test()
            testgenerate = list(zip(question_list, answer_list))
            return jsonify({'cresults': testgenerate})
        else:
            return jsonify({'error': 'Invalid test type'}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
