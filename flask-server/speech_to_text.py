from google.cloud import speech_v1
from pydub import AudioSegment
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account
import wave
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud import storage


from google.cloud import speech_v1
import io

credentials = service_account.Credentials.from_service_account_file(
        'service-account-file.json')
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
        total_text += (alternative.transcript)
    return total_text, words, start_seconds, end_seconds

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json("service-account-file.json")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def run(filepath,audio_file_name):
    import argparse
    bucket_name = "audio-hackcuvi-bucket"
    source_file_name = os.path.join(filepath, audio_file_name)
    destination_blob_name = audio_file_name
    gcs_uri = 'gs://' + bucket_name + '/' + audio_file_name
    upload_blob(bucket_name,source_file_name,destination_blob_name)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
        default=gcs_uri
    )
    args = parser.parse_args()
    return sample_long_running_recognize2(args.storage_uri)
    # print(output)

# if __name__ == "__main__":
##run("", "test.flac")
