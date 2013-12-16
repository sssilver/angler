from flask import Flask, jsonify, request
from flask.ext.cors import origin
app = Flask(__name__)

from student import Student


@app.route("/students", methods=['GET', 'POST', 'PUT'])
@origin(origin='*', headers='Content-Type')
def students():
    student_data = request.get_json()
    student = Student()
    
    return jsonify(student)

if __name__ == "__main__":
    app.run()
