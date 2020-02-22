# audiotsm
# ffmpeg-python

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

from parser import *


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def _logged_subprocess_call(command):
    logger.debug('Running command: {}'.format(subprocess.list2cmdline(command)))
    return subprocess.call(command, shell=True)  # TODO: change to output to logger

    #res = Popen(command, stdout=PIPE, stderr=PIPE)
    #output = res.stdout.read()
    #logger.debug('Output: {}'.format(output))
    #print(res.returncode)
    #return res.returncode


def create_audio(in_filename, out_filename):
    return _logged_subprocess_call(
        (ffmpeg
         .input(in_filename)
         .audio
         .output(out_filename)
         .overwrite_output()
         .compile() + ['-ac'] + ['1']  # set one audio channel
         )
    )


def sentence_to_cut(sent):
    return {sent.start_time, sent.end_time}


def sentences_to_cuts(sent_array):
    return map(sentence_to_cut, sent_array)


if __name__ == '__main__':  # for if you want to run as command line
    parser = argparse.ArgumentParser(description='Gives a new vido from a video')
    parser.add_argument('in_filename', type=str, help='Input filename (`-` for stdin)')
    parser.add_argument('out_filename', type=str, help='Output filename (e.g. `out.wav`)')

    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--create_audio_file', dest='create_audio', action='store_true', help='If you want to create the audio file')
    parser.add_argument('--create_vido_file', dest='create_vido', action='store_true', help='If you want to create the vido file')
    parser.add_argument('--midstep_filenames', type=str, help='Mid way filename pattern (e.g. `out/chunk_{:04d}.wav`)')
    parser.add_argument('--timestamps_file', type=str, help='json file of time stamps to make vido with.')

    kwargs = vars(parser.parse_args())

    # os.path.join(base_dir, filename)

    if kwargs['verbose']:
        logging.basicConfig(level=logging.DEBUG, format='%(levels): %(message)s')
        logger.setLevel(logging.DEBUG)

    if kwargs['create_audio']:
        create_audio(kwargs['in_filename'], kwargs['out_filename'])

    if kwargs['create_vido']:
        pass
