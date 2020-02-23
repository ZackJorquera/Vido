import json
import re
import speech_to_text


class Sentence(object): # Ian wants a list of sentences
    def __init__(self, text, start_time, end_time, lenght):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.length = lenght
    val = 0

#copied from https://stackoverflow.com/questions/4576077/how-to-split-a-text-into-sentences
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
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
    pos = 0
    #turn sentences into objects
    sentenceList = []
    for i in sentences:
        senLen = len(re.split(' |-', str(i)))
        sentenceList.append(Sentence(i, 0, 0, senLen))

    for i in sentenceList:
        #find first word of sentence
        if i.length > 2:
            first, *middle, last = i.text.split()
            last = last[:-1]

            #find corresponding first word
            for j in range(pos, len(words)):
                if words[j].lower() == first.lower():
                    pos = j  #update pos
                    i.start_time = start_times[pos] #update start word
                    break

            for j in range(pos, len(words)):
                if words[j].lower() == last.lower():
                    pos = j         #update pos
                    i.end_time = end_times[pos] #update start word
                    break


    #makes it good for ian
    for i in sentenceList:
        i.text = re.sub(r'[ \t\n\r]+', ' ', i.text).lower()

    return sentenceList
transcript, words, start_seconds, end_seconds = speech_to_text.run()
list = parse(transcript,words, start_seconds, end_seconds)
