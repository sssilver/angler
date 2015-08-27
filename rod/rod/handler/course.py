import flask
import rod
import rod.model.course


course = flask.Blueprint('course', __name__)


@course.route('/course', methods=['GET'])
def list_course():
    all_courses = rod.model.course.Course.query.filter_by(is_deleted=False).all()

    return flask.jsonify({
        'items': rod.model.course.CourseSchema(many=True).dump(all_courses).data,
        'count': len(all_courses)
    })
