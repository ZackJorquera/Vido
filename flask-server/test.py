import video_stuff
import parse_words
import speech_to_text
from summarizer import *
from parse_words import *
import os


if __name__ == '__main__':
    # this will grab from preloaded bucket
    # THis is an example of what this file needs

    INFILE = "videos/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].mp4"
    # TODO: use to_working_video_file(file_name)

    flac_file = video_stuff.create_audio(INFILE, os.path.basename(INFILE) + '.flac')

    transcript, words, start_seconds, end_seconds = speech_to_text.run(os.path.dirname(flac_file),
                                                                       os.path.basename(flac_file))

    # THis will then return out sentence list
    sentence_list = parse(transcript, words, start_seconds, end_seconds)

    print([(s.start_time, s.end_time) for s in sentence_list])

    summary = Summarizer(sentence_list)
    res = summary.create_summary(length_of_video=18)

    print(res)