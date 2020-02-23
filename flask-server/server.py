# The server written in flask
# I'm going to start and get something like this working:
#       https://blog.learningdollars.com/2019/11/29/how-to-serve-a-reactapp-with-a-flask-server/
# and the post get stuff

import os
import asyncio
import time

from video_stuff import *
from runner import run_vidoizer

from flask import Flask, render_template, jsonify, abort, request, make_response, send_file, url_for
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


@app.route('/noreact', methods=['GET'])
def start_noreact():
    return render_template("index_noreact.html")


@app.route('/noreact', methods=['POST'])
def start_noreact_post():
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)

    file_path = to_working_video_file(file.filename)
    file.save(file_path)

    out_file = run_vidoizer(file_path, 'out_file.mp4')

    return send_file(out_file, as_attachment=True)  # just in case


@app.route('/videos/<file_name>', methods=['GET'])
def grab_videos_file(file_name):
    print("hello")
    file_name = os.path.join(VIDEO_WORKING_DIR, file_name)
    if os.path.exists(file_name):
        return send_file(file_name)  # allow reading of this file
    else:
        abort(400)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400)

    file = request.files['file']
    if file.filename == '':
        abort(400)

    file_path = to_working_video_file(file.filename)
    file.save(file_path)

    out_file = run_vidoizer(file_path, 'out_file.mp4')
    out_file = os.path.join(VIDEO_WORKING_DIR, os.path.basename(out_file))

    # return send_file(out_file, as_attachment=True)
    return jsonify({'upload_success': True, 'out_file': out_file.replace('\\','/')}) # send file path


@app.route('/download_file', methods=['GET'])
def check_file():
    # we want to poke the task to see if it is done
    # if it is done return the file and remove the task

    abort(404)
    #return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)  # threaded=True,
