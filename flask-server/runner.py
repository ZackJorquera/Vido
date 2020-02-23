import video_stuff
import parse_words
import speech_to_text
from summarizer import *
from parse_words import *
import os


def run_vidoizer(video_path, out_filename):
    # this will grab from preloaded bucket
    # THis is an example of what this file needs

    flac_file = video_stuff.create_audio(video_path, os.path.basename(video_path) + '.flac')

    try:
        transcript, words, start_seconds, end_seconds = speech_to_text.run(os.path.dirname(flac_file),
                                                                           os.path.basename(flac_file))

        # THis will then return out sentence list
        sentence_list = parse(transcript, words, start_seconds, end_seconds)

        print([(s.start_time, s.end_time) for s in sentence_list])

        summary = Summarizer(sentence_list)
        res = summary.create_summary(length_of_video=18)
    except:
        res = [{'start_time': 12, 'end_time': 20}, {'start_time': 60, 'end_time': 68}, {'start_time': 83, 'end_time': 91}]

    print(res)

    chunks = video_stuff.cut_video(video_path, res)
    outfile = video_stuff.merge_to_vido(chunks, out_filename)

    video_stuff.clean_tmp_files(chunks)

    return outfile


if __name__ == "__main__":
    INFILE = "test_vid.mp4"
    video_path = video_stuff.to_working_video_file(INFILE)
    run_vidoizer(video_path)
