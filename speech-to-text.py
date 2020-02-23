from google.cloud import speech_v1

GOOGLE_APPLICATION_CREDENTIALS = "service-account-file.json"
def sample_long_running_recognize(storage_uri):
    """
    Print start and end time of each word spoken in audio file from Cloud Storage

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.flac'

    # When enabled, the first result returned by the API will include a list
    # of words and the start and end time offsets (timestamps) for those words.
    enable_word_time_offsets = True

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "enable_word_time_offsets": enable_word_time_offsets,
        "language_code": language_code,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    print(response)
    # The first result includes start and end time word offsets
    result = response.results[0]
    # First alternative is the most probable result
    alternative = result.alternatives[0]
    print(u"Transcript: {}".format(alternative.transcript))
    # Print the start and end time of each word
    return alternative

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
        default="gs://cloud-samples-data/speech/brooklyn_bridge.wav",
    )
    args = parser.parse_args()

    output = sample_long_running_recognize(args.storage_uri)


if __name__ == "__main__":
    main()
