import speech_to_text
words = []
start_nanoseconds = []
def itemize():
    output = speech_to_text.sample_long_running_recognize(args.storage_uri)
    for word in alternative.words:
        print(u"Word: {}".format(word.word))
        words.append(word.word)
        print(
            u"Start time: {} seconds {} nanos".format(
                word.start_time.seconds, word.start_time.nanos
            )
        )
        start_nanoseconds.append(word.end_time.seconds + word.end_time.nanos/1e+9)
        print(
            u"End time: {} seconds {} nanos".format(
                word.end_time.seconds, word.end_time.nanos
            )
        )
