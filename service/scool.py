from flask import Flask, jsonify
from flask.ext.cors import origin
app = Flask(__name__)

from student import Student


@app.route("/students", methods=['GET', 'POST', 'PUT'])
@origin(origin='*', headers='Content-Type')
def students():
    return jsonify(status='OK')

if __name__ == "__main__":
    app.run()
