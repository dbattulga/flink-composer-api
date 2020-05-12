import markdown
import os
import shelve
import logging

from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from job_registry import restfunctions
from visualizer import net_graph

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

@app.route("/graph")
def draw():
    net_graph.draw_undirected()


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

        shelf = get_db()
        # Parse the arguments into an object
        args = parser.parse_args()
        job = args['job_name']

        if job in shelf:
            app.logger.info('the job is already running')
            if args['flink_address'] == shelf[job]['location']:
                job_status = restfunctions.check_job_state(args['flink_address'], shelf[job]['jobid'])
                if job_status == 'RUNNING':
                    if shelf[job]['version'] == args['version']:
                        # if version is different, something's changed inside java code
                        if (shelf[job]['mqtt'] != args['mqtt_address'] or
                                shelf[job]['source'] != args['source_topic'] or
                                shelf[job]['sink'] != args['sink_topic'] or
                                shelf[job]['class'] != args['entry_class']):
                            app.logger.info('start from old jar with new parameters')
                            temp = shelf[job]
                            restfunctions.stop_job(shelf[job]['location'], shelf[job]['jobid'])
                            temp['jobid'] = restfunctions.start_jar(shelf[job]['location'],
                                                                      shelf[job]['jarid'],
                                                                      args['entry_class'],
                                                                      args['mqtt_address'],
                                                                      args['source_topic'],
                                                                      args['sink_topic'],
                                                                      args['job_name'])
                            temp['mqtt'] = args['mqtt_address']
                            temp['source'] = args['source_topic']
                            temp['sink'] = args['sink_topic']
                            temp['class'] = args['entry_class']
                            shelf[job] = temp
                        else:
                            app.logger.info('nothing is changed for the job')
                    else:
                        restfunctions.delete_jar(shelf[job]['location'], shelf[job]['jarid'])
                        restfunctions.stop_job(shelf[job]['location'], shelf[job]['jobid'])
                        del shelf[job]
                        key, values = add_job(args)
                        shelf[key] = values
                        app.logger.info('started the job from new jar')
                else:
                    app.logger.info('something wrong, check Flink instances')
            else:
                restfunctions.delete_jar(shelf[job]['location'], shelf[job]['jarid'])
                restfunctions.stop_job(shelf[job]['location'], shelf[job]['jobid'])
                del shelf[job]
                key, values = add_job(args)
                shelf[key] = values
                app.logger.info('job migrated')
        else:
            key, values = add_job(args)
            shelf[key] = values
            app.logger.info(key, values)

        return {'message': 'Job registered', 'data': args}, 201

    def delete(self):
        shelf = get_db()
        keys = list(shelf.keys())
        for key in keys:
            del shelf[key]
        return {'message': 'All deleted', 'data': {}}, 200

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

        restfunctions.delete_jar(shelf[name]['location'], shelf[name]['jarid'])
        restfunctions.stop_job(shelf[name]['location'], shelf[name]['jobid'])
        del shelf[name]
        return '', 204

api.add_resource(Jobs, '/jobs')
api.add_resource(Job, '/jobs/<string:name>')