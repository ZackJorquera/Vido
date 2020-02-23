# audiotsm
# ffmpeg-python

# -v --create_vido_file --midstep_filenames "videos/chunk_{0}.{1}" --timestamps_file "videos/data.json" videos/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].mp4 videos/test_out1.mp4
# -v --create_audio_file videos/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].mp4 videos/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].flac

from __future__ import unicode_literals

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

from parse_words import Sentence


# TODO: remove videos folder and add automatic

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def _logged_subprocess_call(command):
    logger.debug('Running command: {}'.format(subprocess.list2cmdline(command)))
    return subprocess.call(command, shell=True)  # TODO: change to output to logger

    #res = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    #output = res.stdout.read()
    #logger.debug('Output: {}'.format(output))
    #print(res.returncode)
    #return res.returncode


def create_audio(in_filename, out_filename):
    output_kwargs = {}
    output_kwargs['ac'] = 1  # TODO: add bellow and test

    cmd = ffmpeg.input(in_filename).audio.output(out_filename, **output_kwargs).overwrite_output().compile()  # + ['-ac'] + ['1']

    return _logged_subprocess_call(cmd)


def cut_video(in_filename, cuts, midstep_filenames='videos/chunk_{0}.{1}'):
    i = 0
    chunks = []
    for cut in cuts:
        start_time = int(cut['start_time'])
        end_time = int(cut['end_time'])
        i = i+1

        input_kwargs = {}
        input_kwargs['ss'] = start_time  # start time in
        input_kwargs['t'] = end_time - start_time

        file_type = in_filename.split('.')[-1]
        chunk_name = midstep_filenames.format(i, file_type)

        chunks.append(chunk_name)

        cmd = ffmpeg.input(in_filename, **input_kwargs).output(chunk_name).overwrite_output().compile()
        ret = _logged_subprocess_call(cmd)
    return chunks


def merge_to_vido(chunks, out_filename, tmp_file="videos/merge_vids_{0}.txt"):
    tmp_file = tmp_file.format("rand_string")
    with open(tmp_file, 'w') as fw:
        fw.writelines(map(lambda s: 'file \'' + os.path.basename(s) + '\'\n', chunks))

    input_kwargs = {}
    input_kwargs['f'] = 'concat'
    input_kwargs['safe'] = 0
    output_kwargs = {}
    output_kwargs['c'] = 'copy'

    cmd = ffmpeg.input(tmp_file, **input_kwargs).output(out_filename, **output_kwargs).overwrite_output().compile()
    ret = _logged_subprocess_call(cmd)

    os.remove(tmp_file)

    return ret


def clean_tmp_files(chunks):
    for file in chunks:
        os.remove(file)


def sentence_to_cut(sentence):
    try:
        return {'start_time': sentence.start_time / 1000, 'end_time': sentence.end_time / 1000}  # was in ns, we want secs
    except:
        return {'start_time': sentence['start_time'] / 1000, 'end_time': sentence['end_time'] / 1000}  # was in ns, we want secs


def sentences_to_cuts(sentence_array):
    return list(map(sentence_to_cut, sentence_array))


if __name__ == '__main__':  # for if you want to run as command line
    parser = argparse.ArgumentParser(description='Gives a new vido from a video')
    parser.add_argument('in_filename', type=str, help='Input filename (`-` for stdin)')
    parser.add_argument('out_filename', type=str, help='Output filename (e.g. `out.wav`)')

    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--create_audio_file', dest='create_audio', action='store_true', help='If you want to create the audio file')
    parser.add_argument('--create_vido_file', dest='create_vido', action='store_true', help='If you want to create the vido file')
    parser.add_argument('--midstep_filenames', type=str, help='Mid way filename pattern (e.g. `videos/chunk_{0}.{1}}`)')
    parser.add_argument('--timestamps_file', type=str, help='json file of time stamps to make vido with.')

    kwargs = vars(parser.parse_args())

    # os.path.join(base_dir, filename)

    if kwargs['verbose']:
        logging.basicConfig(level=logging.DEBUG, format='%(levels): %(message)s')
        logger.setLevel(logging.DEBUG)

    if kwargs['create_audio']:
        create_audio(kwargs['in_filename'], kwargs['out_filename'])

    if kwargs['create_vido']:
        with open(kwargs['timestamps_file'], 'r') as content_file:
            data = json.load(content_file)

        chunks = cut_video(kwargs['in_filename'], sentences_to_cuts(data['data']), kwargs['midstep_filenames'])
        merge_to_vido(chunks, kwargs['out_filename'])
