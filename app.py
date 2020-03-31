import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'trainingDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI_TASK', 'mongodb://localhost')



@app.route('/')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', "5000")),
            debug=True)