# audiotsm
# ffmpeg-python

# -v --create_vido_file --midstep_filenames "chunk_{0}.{1}" --timestamps_file "videos/data.json" videos/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].mp4 test_out1.mp4
# -v --create_audio_file videos/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].mp4 How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].flac

# from __future__ import unicode_literals

import argparse
import errno
import ffmpeg  # get ffmpeg-python and then download https://ffmpeg.org/download.html
import logging
import os
import re
import subprocess
from subprocess import PIPE, Popen
import sys
import shlex
import json
import time

# from parse_words import Sentence

VIDEO_WORKING_DIR = "videos"


# TODO: remove videos folder and add automatic

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def to_working_video_file(file_name):
    if not os.path.exists(VIDEO_WORKING_DIR):
        os.makedirs(VIDEO_WORKING_DIR)

    new_file_loc = os.path.join(VIDEO_WORKING_DIR, os.path.basename(file_name))

    return new_file_loc


def _logged_subprocess_call(command):
    logger.debug('Running command: {}'.format(subprocess.list2cmdline(command)))
    return subprocess.call(command, shell=True)  # TODO: change to output to logger

    #res = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    #output = res.stdout.read()
    #logger.debug('Output: {}'.format(output))
    #print(res.returncode)
    #return res.returncode


def create_audio(in_filename, out_filename):
    out_filename = os.path.join(VIDEO_WORKING_DIR, out_filename)

    output_kwargs = {'ac': 1}

    cmd = ffmpeg.input(in_filename).audio.output(out_filename, **output_kwargs).overwrite_output().compile()

    _logged_subprocess_call(cmd)

    return os.path.abspath(out_filename)


def cut_video(in_filename, cuts, midstep_filenames='chunk_{0}.{1}'):
    i = 0
    chunks = []
    for cut in cuts:
        start_time = int(cut['start_time']) / 1000
        end_time = int(cut['end_time']) / 1000
        i = i+1

        input_kwargs = {}
        input_kwargs['ss'] = start_time  # start time in
        input_kwargs['t'] = end_time - start_time

        file_type = in_filename.split('.')[-1]
        chunk_name = os.path.join(VIDEO_WORKING_DIR, midstep_filenames.format(i, file_type))

        chunks.append(chunk_name)

        cmd = ffmpeg.input(in_filename, **input_kwargs).output(chunk_name).overwrite_output().compile()
        ret = _logged_subprocess_call(cmd)

    return chunks


def merge_to_vido(chunks, out_filename, tmp_file="merge_vids_{0}.txt"):
    out_filename = os.path.join(VIDEO_WORKING_DIR, out_filename)

    tmp_file = os.path.join(VIDEO_WORKING_DIR, tmp_file.format("rand_string"))
    with open(tmp_file, 'w') as fw:
        # fw.writelines(map(lambda s: 'file \'' + os.path.basename(s) + '\'\n', chunks))
        fw.writelines(map(lambda s: 'file \'' + s + '\'\n', chunks))

    input_kwargs = {'f': 'concat', 'safe': 0}
    output_kwargs = {'c': 'copy'}

    cmd = ffmpeg.input(tmp_file, **input_kwargs).output(out_filename, **output_kwargs).overwrite_output().compile()
    ret = _logged_subprocess_call(cmd)

    os.remove(tmp_file)

    return os.path.abspath(out_filename)


def clean_tmp_files(chunks):
    for file in chunks:
        os.remove(file)


if __name__ == '__main__':  # for if you want to run as command line
    parser = argparse.ArgumentParser(description='Gives a new vido from a video')
    parser.add_argument('in_filename', type=str, help='Input filename (`-` for stdin)')
    parser.add_argument('out_filename', type=str, help='Output filename (e.g. `out.wav`)')

    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--create_audio_file', dest='create_audio', action='store_true', help='If you want to create the audio file')
    parser.add_argument('--create_vido_file', dest='create_vido', action='store_true', help='If you want to create the vido file')
    parser.add_argument('--midstep_filenames', type=str, help='Mid way filename pattern (e.g. `chunk_{0}.{1}}`)')
    parser.add_argument('--timestamps_file', type=str, help='json file of time stamps to make vido with.')

    kwargs = vars(parser.parse_args())

    # os.path.join(base_dir, filename)

    if kwargs['verbose']:
        logging.basicConfig(level=logging.DEBUG, format='%(levels): %(message)s')
        logger.setLevel(logging.DEBUG)

    if kwargs['create_audio']:
        out_path = create_audio(kwargs['in_filename'], kwargs['out_filename'])

    if kwargs['create_vido']:
        with open(kwargs['timestamps_file'], 'r') as content_file:
            data = json.load(content_file)

        chunks = cut_video(kwargs['in_filename'], data['data'], kwargs['midstep_filenames'])
        out_path = merge_to_vido(chunks, kwargs['out_filename'])
