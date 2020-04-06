import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'trainingDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI_MILESTONE3', 'mongodb://localhost')

mongo = PyMongo(app)

# Course Related CRUD Functionality


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
    courses = mongo.db.courses
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


@app.route('/delete_course/<course_id>')
def delete_course(course_id):
    mongo.db.courses.remove({'_id': ObjectId(course_id)})
    return redirect(url_for('get_courses'))

# Category Related CRUD Functionality

@app.route('/get_categories')
def get_categories():
    return render_template("categories.html", categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template("addcategory.html")
    

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))

# Course Duration Related CRUD Functionality


@app.route('/get_durations')
def get_durations():
    return render_template("durations.html", durations=mongo.db.course_duration.find())


@app.route('/edit_duration/<duration_id>')
def edit_duration(duration_id):
    return render_template('editduration.html',
    duration=mongo.db.course_duration.find_one({'_id': ObjectId(duration_id)}))


@app.route('/update_duration/<duration_id>', methods=['POST'])
def update_duration(duration_id):
    mongo.db.course_duration.update_one(
        {'_id': ObjectId(duration_id)},
        {'duration': request.form.get('duration')})
    return redirect(url_for('get_durations'))


@app.route('/delete_duration/<duration_id>')
def delete_duration(duration_id):
    mongo.db.course_duration.remove({'_id': ObjectId(duration_id)})
    return redirect(url_for('get_durations'))

# Course Size Related CRUD Functionality
@app.route('/get_sizes')
def get_sizes():
    return render_template("sizes.html", sizes=mongo.db.course_sizes.find())


@app.route('/edit_size/<size_id>')
def edit_size(size_id):
    return render_template('editsize.html',
    size=mongo.db.course_sizes.find_one({'_id': ObjectId(size_id)}))


@app.route('/update_size/<size_id>', methods=['POST'])
def update_size(size_id):
    mongo.db.course_sizes.update_one(
        {'_id': ObjectId(size_id)},
        {'max_subscriber': request.form.get('max_subscriber')})
    return redirect(url_for('get_sizes'))


@app.route('/delete_size/<size_id>')
def delete_size(size_id):
    mongo.db.course_sizes.remove({'_id': ObjectId(size_id)})
    return redirect(url_for('get_sizes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)