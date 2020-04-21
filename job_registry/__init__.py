import markdown
import os
import shelve

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("jobs.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)

class JobsList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        jobs = []
        for key in keys:
            jobs.append(shelf[key])
        return {'message': 'Success', 'data': jobs}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('job_name', required=True)
        parser.add_argument('version', required=True)
        parser.add_argument('flink_address', required=True)
        parser.add_argument('mqtt_address', required=True)
        parser.add_argument('source_topic', required=True)
        parser.add_argument('sink_topic', required=True)
        parser.add_argument('entry_class', required=True)
        parser.add_argument('jar_path', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        shelf = get_db()
        shelf[args['job_name']] = args
        return {'message': 'Job registered', 'data': args}, 201

class Job(Resource):
    def get(self, name):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (name in shelf):
            return {'message': 'Job not found', 'data': {}}, 404

        return {'message': 'Job found', 'data': shelf[name]}, 200

    def delete(self, name):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (name in shelf):
            return {'message': 'Job not found', 'data': {}}, 404

        del shelf[name]
        return '', 204

api.add_resource(JobsList, '/jobs')
api.add_resource(Job, '/jobs/<string:name>')