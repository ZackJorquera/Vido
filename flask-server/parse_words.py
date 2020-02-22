import re

class Sentence(object):
    def __init__(self, text):
        self.text = text
        self.length = len(re.split(' |-', text))

    def __str__(self):
        return str(self.text)
    start_time = 0
    end_time = 0
    val = 0


def test(s):
    print(s)


if __name__ == '__main__':
    pass

# Ian wants a list of sentences