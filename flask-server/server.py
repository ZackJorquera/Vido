# The server written in flask
# I'm going to start and get something like this working:
#       https://blog.learningdollars.com/2019/11/29/how-to-serve-a-reactapp-with-a-flask-server/
# and the post get stuff

import os
import asyncio
import time

from video_stuff import *

helper_tasks = []  # type tuple of id, task, and ret val
id_iter = 0

from flask import Flask, render_template, jsonify, abort, request, make_response, url_for
# from flask_cors import CORS  # is this needed

app = Flask(__name__)
app.secret_key = "Not Random. Oh Noes!"  # This is for metadata encryption

# CORS(app)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/')
def start():
    return render_template("index.html")  # react will make index.html


def task_run_vido_stuff(start_file):
    time.sleep(10)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400)

    file = request.files['file']
    if file.filename == '':
        abort(400)

    file_path = to_working_video_file(file.filename)
    file.save(file_path)

    id_iter += 1
    helper_tasks.append( (id_iter, asyncio.create_task( task_run_vido_stuff(file_path) )) )
    return jsonify({'upload_success': True, 'task_id': id_iter})


@app.route('/check_file', methods=['GET'])
def check_file():
    # we want to poke the task to see if it is done
    # if it is done return the file and remove the task
    if 'task_id' not in request:
        abort(400)

    task_id = request['task_id']

    task_filt = filter(lambda id, task: id == task_id, helper_tasks)
    if len(task_filt) == 0:
        abort(400)

    id, task = task_filt[0]

    file_ready = task.done()
    if file_ready:
        res_path = task.result()
    else:
        res_path = ""

    return jsonify({'file_ready': file_ready, 'file': res_path})


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)
