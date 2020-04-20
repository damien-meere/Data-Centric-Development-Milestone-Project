import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import date, datetime

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'trainingDB'
app.config["MONGO_URI"] = os.getenv(
    'MONGO_URI_MILESTONE3', 'mongodb://localhost')

mongo = PyMongo(app)

# Course Related CRUD Functionality

@app.route('/')
@app.route('/get_courses_gte')
def get_courses_gte():
    """
    Upcoming Courses
    Call to courses page and supply list of all courses that will run after today, sorted by date
    """
    # get todays date
    today = date.today()
    # get date in correct string format
    today_string = today.strftime("%Y-%m-%d")
    return render_template("courses.html", courses=mongo.db.courses.find({"date":{'$gte': today_string}}).sort("date", 1))



@app.route('/get_courses_lt')
def get_courses_lt():
    """
    Complete Courses
    Call to courses page and supply list of all courses that ran before today, sorted by date
    """
    # get todays date
    today = date.today()
    # get date in correct string format
    today_string = today.strftime("%Y-%m-%d")
    return render_template("courses.html", courses=mongo.db.courses.find({"date":{'$lt': today_string}}).sort("date", 1))



@app.route('/get_all_courses')
def get_all_courses():
    #Call to courses page and supply list of all courses, regardless of start date
    return render_template("courses.html", courses=mongo.db.courses.find().sort("date", 1))



@app.route('/get_trainee_courses')
def get_trainee_courses():
    """
    Call to trainee courses page and supply list of all courses coming up (not showing previous courses for this iteration)
    """

    # get todays date
    today = date.today()
    # get date in correct string format
    today_string = today.strftime("%Y-%m-%d")
    return render_template("courses_trainee.html", courses=mongo.db.courses.find({"date":{'$gte': today_string}}).sort("date", 1))


@app.route('/add_course')
def add_course():
    """
    Call to add course page, supplying options for dropdown menu from
    collections in db (category, duration, size)
    """
    get_categories = mongo.db.categories.find()
    get_durations = mongo.db.course_duration.find()
    get_sizes = mongo.db.course_sizes.find()
    return render_template('addcourse.html',
                           categories=get_categories,
                           durations=get_durations,
                           sizes=get_sizes)


@app.route('/insert_course', methods=['POST'])
def insert_course():
    # Insert new course to database, pull requisit data from request object
    courses = mongo.db.courses
    """
    HTML Form cannot inject an Array object, therefore when creating a new
    course, we have to edit the dict object to initiate the course with the
    subscriber_list field set as an empty array.
    """
    course_insertion = request.form.to_dict()
    course_insertion.update({'subscriber_list': []})
    course_insertion.update({'percentage': "0%"})
    courses.insert_one(course_insertion)
    return redirect(url_for('get_courses_gte'))



@app.route('/update_course/<course_id>')
def update_course(course_id):
    """
    Call to editcourse page with requisite data from
    collections in db (category, duration, size)
    """
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
    coursedb = mongo.db.courses
    """
    Editing a previously created course object.
    $set operator required to ensure we only update the requisite fields, and
    not create an entirely  new object in the database containing only the data from the
    request.
    """
    coursedb.update_one({'_id': ObjectId(course_id)},
                        {"$set": {
                            'category_name': request.form.get('category_name'),
                            'course_name': request.form.get('course_name'),
                            'date': request.form.get('date'),
                            'duration': request.form.get('duration'),
                            'course_description': request.form.get('course_description')
                        }})
    return redirect(url_for('get_courses_gte'))


@app.route('/delete_course/<course_id>')
def delete_course(course_id):
    """
    Delete specified course from database
    Gather specified course ID and call remove function
    """
    mongo.db.courses.remove({'_id': ObjectId(course_id)})
    return redirect(url_for('get_courses_gte'))


## Enrollment-specific functions


@app.route('/enroll_course/<course_id>')
def enroll_course(course_id):
    """
    Call to trainee enrollment page, and harnessing of all information to be 
    presented in the dropdown menus
    """
    course_edit = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    get_categories = mongo.db.categories.find()
    get_durations = mongo.db.course_duration.find()
    get_sizes = mongo.db.course_sizes.find()
    return render_template('enrollcourse.html',
                           course=course_edit,
                           categories=get_categories,
                           durations=get_durations,
                           sizes=get_sizes)



@app.route('/edit_course_enroll/<course_id>', methods=["POST"])
def edit_course_enroll(course_id):
    """
    Here the enrollment form is operted on. Need to first check if the course
    limit has been exceeded by accessing the max subscriber that's been set,
    and the total subscriber number
    """    
    coursedb = mongo.db.courses
    target_course_size = coursedb.find_one(
        {'_id': ObjectId(course_id)}, {"max_subscriber": 1})
    target_course_subscribers = coursedb.find_one(
        {'_id': ObjectId(course_id)}, {"subscriber_list": 1})
    # Cast returned max_subscriber value to Integer for comparison with
    # subscriber number
    max_size = int(target_course_size["max_subscriber"])
    subscribers = len(target_course_subscribers["subscriber_list"])
    # If statement to compare the max course size with current number of
    # subscribers if there's still space add the user to the database
    if subscribers < max_size:
        # need to get the percentage of number of subscribers versus the max
        # subscribers this value will then be placed back within the course
        # object, to be harnassed within the front end to display the
        # subscription level progress bar create subscriber percentage value
        # as a string (increment subscriber total)
        subscribers += 1
        course_percentage = "{:.0%}".format(subscribers/max_size)
        # $push used to add the new user record into the subscriber field without 
        # overwriting what's already in place
        coursedb.update_one({'_id': ObjectId(course_id)},
                            {"$push":
                             {"subscriber_list":
                              {
                                  "user_name": request.form.get('user_name'),
                                  "user_email": request.form.get('user_email')
                              },
                              }
                             }
                            )
        # $set operator required to ensure we only update the requisit fields, and
        # not create a new object in the database containing only the data from the
        # request.
        coursedb.update_one({'_id': ObjectId(course_id)},
                            {"$set": {
                                "percentage": course_percentage
                            }})
        # direct to successful enrollment page
        return redirect(url_for('enrollment_success'))
    else:
        # print ("Course Full")
        # direct to failure page
        return redirect(url_for('enrollment_fail'))


@app.route('/show_enrollments/<course_id>')
def show_enrollments(course_id):
    """
    Show list of enrollments for a course
    Gather specified course ID and call remove function
    """
    course = mongo.db.courses.find_one({'_id': ObjectId(course_id)})
    return render_template('showenrollments.html',
                           course=course)


@app.route('/enrollment_success')
def enrollment_success():
    """
    Display result of successful enrollment
    """
    return render_template("enrollmentsuccess.html")


# display result of unsuccessful enrollment
@app.route('/enrollment_fail')
def enrollment_fail():
    return render_template("enrollmentfail.html")


## Category Related CRUD Functionality


@app.route('/get_categories')
def get_categories():
    """
    Display list of available categories
    """
    return render_template("categories.html", categories=mongo.db.categories.find())



@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    """
    Allow choice of category to edit
    """
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    """
    Edit specific Category information
    """
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))



@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    """
    Delete specified category
    """
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    """
    Call to return add category page
    """
    return render_template("addcategory.html")



@app.route('/insert_category', methods=['POST'])
def insert_category():
    """
    Insert new catagory to database
    """
    categorydb = mongo.db.categories
    category_doc = {'category_name': request.form.get('category_name')}
    categorydb.insert_one(category_doc)
    return redirect(url_for('get_categories'))


# Course Duration Related CRUD Functionality


@app.route('/get_durations')
def get_durations():
    """
    Get duration values from database
    """
    return render_template("durations.html", durations=mongo.db.course_duration.find())


@app.route('/edit_duration/<duration_id>')
def edit_duration(duration_id):
    """
    Allow choice of duration to edit
    """
    return render_template('editduration.html',
                           duration=mongo.db.course_duration.find_one({'_id': ObjectId(duration_id)}))


@app.route('/update_duration/<duration_id>', methods=['POST'])
def update_duration(duration_id):
    """
    edit specified duration
    """
    mongo.db.course_duration.replace_one(
        {'_id': ObjectId(duration_id)},
        {'duration': request.form.get('duration')})
    return redirect(url_for('get_durations'))


@app.route('/delete_duration/<duration_id>')
def delete_duration(duration_id):
    """
    Delete specified duration
    """
    mongo.db.course_duration.remove({'_id': ObjectId(duration_id)})
    return redirect(url_for('get_durations'))


@app.route('/add_duration')
def add_duration():
    """
    Call addduration page
    """
    return render_template("addduration.html")


@app.route('/insert_duration', methods=['POST'])
def insert_duration():
    """
    Insert new duration value to database
    """
    durationdb = mongo.db.course_duration
    duration_doc = {'duration': request.form.get('duration')}
    durationdb.insert_one(duration_doc)
    return redirect(url_for('get_durations'))


# Course Size Related CRUD Functionality


@app.route('/get_sizes')
def get_sizes():
    """
    Get sizes from database
    """
    return render_template("sizes.html", sizes=mongo.db.course_sizes.find())


@app.route('/edit_size/<size_id>')
def edit_size(size_id):
    """
    Allow choice of size value to edit
    """
    return render_template('editsize.html',
                           size=mongo.db.course_sizes.find_one({'_id': ObjectId(size_id)}))


@app.route('/update_size/<size_id>', methods=['POST'])
def update_size(size_id):
    """
    Edit specified size
    """
    mongo.db.course_sizes.replace_one(
        {'_id': ObjectId(size_id)},
        {'max_subscriber': request.form.get('max_subscriber')})
    return redirect(url_for('get_sizes'))


@app.route('/delete_size/<size_id>')
def delete_size(size_id):
    """
    Delete specified size
    """
    mongo.db.course_sizes.remove({'_id': ObjectId(size_id)})
    return redirect(url_for('get_sizes'))


@app.route('/add_size')
def add_size():
    """
    Call to addsize page
    """
    return render_template("addsize.html")


@app.route('/insert_size', methods=['POST'])
def insert_size():
    """
    Insert new size value to database
    """
    sizedb = mongo.db.course_sizes
    size_doc = {'max_subscriber': request.form.get('max_subscriber')}
    sizedb.insert_one(size_doc)
    return redirect(url_for('get_sizes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)
