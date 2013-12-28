from flask import Flask, jsonify, request
from flask.ext.cors import origin
app = Flask(__name__)

from student import Student, Availability


@app.route("/students", methods=['PUT'])
@origin(origin='*', headers='Content-Type')
def students():
    data = dict(request.get_json())
    availabilities_data = data.pop('availabilities')

    availability = []

    for day, ranges in enumerate(availabilities_data):
        for range in ranges:
            availability.append(Availability(**{
                'day': day,
                'range_from': int(range[0]),
                'range_to': int(range[1])
            }))


    data['availability'] = availability

    new_student = Student(**data)
    print new_student
    return jsonify(request.get_json())

if __name__ == "__main__":
    app.run(debug=True)
