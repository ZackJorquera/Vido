import json
import math
import re
import speech_to_text
from summarizer import *


class Sentence(object):
    def __init__(self, text, start_time, end_time, length):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.length = length
        self.val = 0

    def sentence_weight(self, by_time=False):
        if by_time:
            return self.end_time - self.start_time
        else:
            return self.length


# copied from https://stackoverflow.com/questions/4576077/how-to-split-a-text-into-sentences
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def parse(transcript, words, start_times, end_times):
    # words = [item['word'] for item in contents]
    # start_times = [item['startTime'] for item in contents]
    # end_times = [item['endTime'] for item in contents]

    # First alternative is the most probable result
    # Print the start and end time of each word
    sentences = split_into_sentences(transcript)
    print(sentences)
    pos = 0
    # turn sentences into objects
    sentenceList = []
    for i in sentences:
        senLen = len(re.split(' |-', str(i)))

        # This would be
        sentenceList.append(Sentence(i, 0, 0, senLen))

    for i in sentenceList:
        # find first word of sentence
        split_sentence = re.split(' |-', i.text[:-1])
        first = split_sentence[0]
        last = split_sentence[-1]

        # find corresponding first word
        # this heavily assumes the data is perfectly aligned, which seems to be true
        i.start_time = start_times[pos]
        i.end_time = end_times[pos + i.length - 1]
        pos += i.length

    # makes it good for ian
    for i in sentenceList:
        i.text = re.sub(r'[ \t\n\r]+', ' ', i.text).lower()

    return sentenceList


if __name__ == '__main__':
    # this will grab from preloaded bucket
    # THis is an example of what this file needs
    transcript, words, start_seconds, end_seconds = speech_to_text.run()

    # THis will then return out sentence list
    sentence_list = parse(transcript, words, start_seconds, end_seconds)

    print([(s.start_time, s.end_time) for s in sentence_list])

    summary = Summarizer(sentence_list)
    res = summary.create_summary(percent_words=.25)

    print(res)
