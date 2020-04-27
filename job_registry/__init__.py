import markdown
import os
import shelve
import logging

from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from job_registry import restfunctions
from time import sleep

logging.basicConfig(level=logging.DEBUG)
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


def add_job(args):
    jarid = restfunctions.upload_jar(args['flink_address'], args['jar_path'])
    jobid = restfunctions.start_jar(args['flink_address'], jarid, args['entry_class'], args['mqtt_address'],
                                    args['source_topic'], args['sink_topic'], args['job_name'])

    key = args['job_name']
    values = {'jobname': args['job_name'],
                'version': args['version'],
                'jarid': jarid,
                'jobid': jobid,
                'location': args['flink_address'],
                'mqtt': args['mqtt_address'],
                'source': args['source_topic'],
                'sink': args['sink_topic'],
                'class': args['entry_class']
                }
    return key, values


class Jobs(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        jobs = []
        for key in keys:
            jobs.append(shelf[key])
        return {'message': 'Success', 'data': jobs}, 200

    def post(self):
        """shelve can't detect changes in nested mutable objects, re-set the dictionary instead
        shelve will save overwrite values if key exists"""
        parser = reqparse.RequestParser()
        parser.add_argument('job_name', required=True)
        parser.add_argument('version', required=True)
        parser.add_argument('flink_address', required=True)
        parser.add_argument('mqtt_address', required=True)
        parser.add_argument('source_topic', required=True)
        parser.add_argument('sink_topic', required=True)
        parser.add_argument('entry_class', required=True)
        parser.add_argument('jar_path', required=True)

        # args = parser.parse_args()
        # shelf = get_db()
        # shelf[args['job_name']] = args
        # return {'message': 'Device registered', 'data': args}, 201

        # Parse the arguments into an object
        args = parser.parse_args()

        # Call Flink REST API to get jobid jarid
        key, values = add_job(args)
        shelf = get_db()

        # Save it to DB
        shelf[key] = values
        app.logger.info(key, values)

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

api.add_resource(Jobs, '/jobs')
api.add_resource(Job, '/jobs/<string:name>')