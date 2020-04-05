import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'trainingDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI_MILESTONE3', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_courses')
def get_courses():
    return render_template("courses.html", courses=mongo.db.courses.find())

@app.route('/add_course')
def add_course():
    get_categories = mongo.db.categories.find()
    get_durations = mongo.db.course_duration.find()
    get_sizes = mongo.db.course_sizes.find()
    return render_template('addcourse.html', 
        categories=get_categories,
        durations=get_durations,
        sizes=get_sizes)

@app.route('/insert_course', methods=['POST'])
def insert_course():
    courses = mongo.db.courses
    courses.insert_one(request.form.to_dict())
    return redirect(url_for('get_courses'))

@app.route('/update_course/<course_id>')
def update_course(course_id):
    course_edit = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    get_categories = mongo.db.categories.find()
    get_durations = mongo.db.course_duration.find()
    get_sizes = mongo.db.course_sizes.find()
    return render_template('editcourse.html',
        course=course_edit,
        categories=get_categories,
        durations=get_durations,
        sizes=get_sizes)

@app.route('/edit_course/<course_id>', methods=["POST"])
def edit_course(course_id):
    courses=mongo.db.courses
    courses.update({'_id': ObjectId(course_id)},
    {
        'category_name': request.form.get('category_name'),
        'course_name': request.form.get('course_name'),
        'date': request.form.get('date'),
        'duration': request.form.get('duration'),
        'course_description': request.form.get('course_description'),
        'max_subscriber': request.form.get('max_subscriber')
    })
    return redirect(url_for('get_courses'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)