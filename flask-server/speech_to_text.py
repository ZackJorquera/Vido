from google.cloud import speech_v1
from pydub import AudioSegment
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave

GOOGLE_APPLICATION_CREDENTIALS = "service-account-file.json"
def sample_long_running_recognize(storage_uri):
    """
    Print start and end time of each word spoken in audio file from Cloud Storage

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    #file_name = filepath + audio_file_name
    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.flac'

    # When enabled, the first result returned by the API will include a list
    # of words and the start and end time offsets (timestamps) for those words.
    enable_word_time_offsets = True
    enable_automatic_punctuation = True

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "enable_word_time_offsets": enable_word_time_offsets,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "language_code": language_code,
    }
    audio = {"uri": storage_uri}

    operation = client.recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    # The first result includes start and end time word offsets
    result = response.results[0]
    print(result)
    # First alternative is the most probable result
    alternative = result.alternatives[0]
    print(u"Transcript: {}".format(alternative.transcript))
    # Print the start and end time of each word
    for word in alternative.words:
        print(u"Word: {}".format(word.word))
        words.append(word.word)
        print(
            u"Start time: {} seconds {} nanos".format(
                word.start_time.seconds, word.start_time.nanos
            )
        )
        start_seconds.append(word.start_time.seconds + word.start_time.nanos/1e+9)
        print(
            u"End time: {} seconds {} nanos".format(
                word.end_time.seconds, word.end_time.nanos
            )
        )
        start_seconds.append(word.end_time.seconds + word.end_time.nanos/1e+9)
    return alternative.words
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

from google.cloud import speech_v1
import io

def sample_long_running_recognize2(storage_uri):
    client = speech_v1.SpeechClient()
    words = []
    start_seconds = []
    end_seconds = []
    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"
    enable_word_time_offsets = True
    enable_automatic_punctuation = True
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    config = {
        "enable_word_time_offsets": enable_word_time_offsets,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    print(response)
    total_text = ''
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        for word in alternative.words:
            print(u"Word: {}".format(word.word))
            words.append(word.word)
            print(
                u"Start time: {} seconds {} nanos".format(
                    word.start_time.seconds, word.start_time.nanos
                )
            )
            start_seconds.append(word.start_time.seconds + word.start_time.nanos/1e+9)
            print(
                u"End time: {} seconds {} nanos".format(
                    word.end_time.seconds, word.end_time.nanos
                )
            )
            end_seconds.append(word.end_time.seconds + word.end_time.nanos/1e+9)
        print(u"Transcript: {}".format(alternative.transcript))
        total_text += (alternative.transcript + ".")
    return total_text, words, start_seconds, end_seconds

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
def run():
    import argparse
    # bucket_name = "audio-hackcuvi-bucket"
    # source_file_name = filepath + audio_file_name
    # destination_blob_name = audio_file_name
    # gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
        default="gs://audio-hackcuvi-bucket/How_virtual_reality_turns_students_into_scientists_Jessica_Ochoa_Hendrix[youtubetomp4.org].flac"
    )
    args = parser.parse_args()
    return sample_long_running_recognize2(args.storage_uri)
    # print(output)

# if __name__ == "__main__":
#     run()
