import re


class Word(object):
    word = ""
    start_time = 0
    end_time = 0


class Sentence(object):
    words = []
    start_time = 0
    end_time = 0
    val = 0


# Function Ian thinks might be useful
def clean_word(w):
    return re.sub(r'[^\w]', '', w.strip().lower())

# Ian wants a list of sentences