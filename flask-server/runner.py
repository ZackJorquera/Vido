import video_stuff
import parse_words
import speech_to_text
from summarizer import *
from parse_words import *
import os
import json


def merge_cut_time(cuts):
    i = 1
    while i < len(cuts):
        if cuts[i - 1]['end_time'] == cuts[i]['start_time']:
            cuts[i - 1]['end_time'] = cuts[i]['end_time']
            del cuts[i]
        else:
            i += 1
    return cuts


def run_vidoizer(video_path, out_filename):
    # this will grab from preloaded bucket
    # THis is an example of what this file needs

    flac_file = video_stuff.create_audio(video_path, os.path.basename(video_path) + '.flac')

    #try:
    transcript, words, start_seconds, end_seconds = speech_to_text.run(os.path.dirname(flac_file),
                                                                       os.path.basename(flac_file))

    # THis will then return out sentence list
    sentence_list = parse(transcript, words, start_seconds, end_seconds)

    print([(s.start_time, s.end_time) for s in sentence_list])

    summary = Summarizer(sentence_list)
    res = summary.create_summary(length_of_video=180)

    res = merge_cut_time(res)
    #except:
        #res = [{'start_time': 12, 'end_time': 20}, {'start_time': 60, 'end_time': 68}, {'start_time': 83, 'end_time': 91}]

    print(res)

    with open('cached_vid.json', 'w') as fp:
        json.dump(res, fp)

    chunks = video_stuff.cut_video(video_path, res)
    outfile = video_stuff.merge_to_vido(chunks, out_filename)

    video_stuff.clean_tmp_files(chunks, flac_file)

    return outfile

if __name__ == "__main__":
    data = [{"start_time": 14.1, "end_time": 19.9, "text": "vicky to express vpn for sponsoring today's episode of stay tuned to the end to learn how you can get your first 3 months free"}, {"start_time": 19.9, "end_time": 21.5, "text": "hey, what's up everyone"}, {"start_time": 21.5, "end_time": 23.6, "text": "welcome back to another episode of visual effects artist"}, {"start_time": 40.0, "end_time": 43.7, "text": "there's not a lot of finals but for everything, i've done a lot of temp work"}, {"start_time": 43.7, "end_time": 45.8, "text": "i think we'll be taking a look at some of those today"}, {"start_time": 51.4, "end_time": 53.8, "text": "i'm a big fan of like smoke simulations"}, {"start_time": 53.8, "end_time": 55.8, "text": "and those are some really cool smoke simulation"}, {"start_time": 55.8, "end_time": 61.0, "text": "they were actually supposed to always have a bit of steam or smoke and i actually found this reference"}, {"start_time": 61.0, "end_time": 73.3, "text": "i was like a warm horse on a winter cold winter day, but then as you get closer and closer to deadlines, it's just like smoke simulations take forever to calculate"}, {"start_time": 73.3, "end_time": 86.5, "text": "it was really hard actually getting that look right because i didn't want it to seem like it's geometry but just smoke comes out of when they turn into smells like i wanted to feel that snow"}, {"start_time": 86.5, "end_time": 88.4, "text": "they actually turn into smoke"}, {"start_time": 92.7, "end_time": 94.9, "text": "the boardroom scene was actually a reshoot"}, {"start_time": 94.9, "end_time": 98.4, "text": "they had to really hurry to get that done in time"}, {"start_time": 98.4, "end_time": 99.6, "text": "and it was a thing"}, {"start_time": 151.7, "end_time": 154.0, "text": "they were just there for something to look at it"}, {"start_time": 176.3, "end_time": 177.4, "text": "we have a son guy in there"}, {"start_time": 185.0, "end_time": 186.2, "text": "i highly recommend you check it out"}, {"start_time": 186.2, "end_time": 189.1, "text": "but there's one thing in particular that blew me away"}, {"start_time": 216.9, "end_time": 220.4, "text": "you just get blind too because of course we're looking at him is he looking"}, {"start_time": 240.5, "end_time": 247.3, "text": "you can still tell like okay, this is where he was at a few kids like you don't get that fluid movement"}, {"start_time": 251.9, "end_time": 267.7, "text": "so it is sometimes it's like well maybe we should have just knocked shotted with him and just done it all cgi, but at the same time you do get a lot of reference for poor lighting and everything so exactly what it should look like cuz he filmed it for real even if it's not being used"}, {"start_time": 267.7, "end_time": 274.1, "text": "i think they were able to actually take his real head and put it on there because the cg had didn't look quite right"}, {"start_time": 274.1, "end_time": 279.7, "text": "okay body and don't look fake but just the head like just a head stands out"}, {"start_time": 290.0, "end_time": 294.1, "text": "looks like it floats around a bit"}, {"start_time": 314.8, "end_time": 318.1, "text": "well for one, it's the rock's head is coming separately from the body"}, {"start_time": 440.7, "end_time": 446.9, "text": "so they had to project the images onto that to get proper like parallax of the reflections in addition to that"}, {"start_time": 446.9, "end_time": 449.7, "text": "they actually put a gopro on his face really for all of that"}, {"start_time": 468.3, "end_time": 479.0, "text": "turn off the camera except for the fact that they couldn't get a material that can do both be stretchy enough to fit over his head and also be reflective enough to be that near like effect"}, {"start_time": 484.2, "end_time": 492.0, "text": "i'm just thinking like, oh, i wonder if they had to cut scenes with looking glass because it was his studio was like all these expensive things with him"}, {"start_time": 513.3, "end_time": 516.3, "text": "there is a guest that you think we should get on the show"}, {"start_time": 578.3, "end_time": 579.7, "text": "it's those jaws"}, {"start_time": 605.1, "end_time": 611.1, "text": "scared but i just can't help it be pulled out of it doesn't look like the sharks there at all"}, {"start_time": 676.6, "end_time": 679.0, "text": "there's no way so you're suggesting that they painted it"}, {"start_time": 679.0, "end_time": 679.4, "text": "i don't know"}, {"start_time": 679.4, "end_time": 681.6, "text": "it's almost to smooth but i move"}, {"start_time": 681.6, "end_time": 683.8, "text": "yeah, it's almost like a 2d animation"}, {"start_time": 700.5, "end_time": 702.3, "text": "this movie's almost 40 years old"}, {"start_time": 728.5, "end_time": 732.4, "text": "hi, my name is sam gorski co-founder of corridordigital"}, {"start_time": 737.6, "end_time": 738.3, "text": "that's pretty good"}, {"start_time": 738.3, "end_time": 740.5, "text": "that's really nice and smooth intro"}, {"start_time": 753.6, "end_time": 754.1, "text": "it is good"}, {"start_time": 770.0, "end_time": 771.9, "text": "i totally noticed, you know the privacy"}, {"start_time": 790.0, "end_time": 791.8, "text": "this is my favorite part right here"}, {"start_time": 813.9, "end_time": 819.2, "text": "com corridor crew, you'll get 3 months free just by signing up with the link in the description below"}, {"start_time": 821.8, "end_time": 822.6, "text": "i better be careful"}, {"start_time": 822.6, "end_time": 824.0, "text": "you might almost put me out of a job here"}, {"start_time": 824.0, "end_time": 826.9, "text": "i mean, next time brandi o'daniel catch you on the flip side"}, {"start_time": 845.2, "end_time": 846.0, "text": "i help you pick it up"}]
    merge_cut_time(data)

    INFILE = "test_vid.mp4"
    video_path = video_stuff.to_working_video_file(INFILE)
    run_vidoizer(video_path, "out_file.mp4")
