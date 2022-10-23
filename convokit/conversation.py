import json
from pathlib import Path

import pandas as pd
from convokit import Coordination, Corpus, Speaker, Utterance
from google.cloud import speech


def dump_transcript(in_file: Path, out_file: Path) -> None:
    """Get transcript from Google Speech-to-Text API"""
    client = speech.SpeechClient()

    content = Path("long.wav").read_bytes()
    audio = speech.RecognitionAudio(content=content)

    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=2,
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        sample_rate_hertz=48000,
        diarization_config=diarization_config,
        enable_word_time_offsets=True,
        model="video",
    )
    conversation = []
    response = client.recognize(config=config, audio=audio)

    alternative = response.results[-1].alternatives[0]
    for word_info in alternative.words:
        conversation.append(
            {
                "speaker": word_info.speaker_tag,
                "text": word_info.word,
                "timestamp": word_info.start_time.total_seconds(),
            }
        )

    with output.open("w") as f:
        json.dump(conversation, f, indent=2)

def assemble_corpus(out_file: Path) -> Corpus:
  """Assemble corpus from annotated transcript"""
    conversation = json.load(out_file.open())

    df = pd.DataFrame(conversation)
    df["id"] = df.index
    df["speaker"] = df["speaker"].astype(str)
    df["reply_to"] = df.apply(lambda x: "2" if x["speaker"] == "1" else "1", axis=1)
    df["conversation_id"] = 1

    return Corpus.from_pandas(df)

if __name__ == "__main__":
  in_file = Path("audio/long.wav")
  out_file = Path("transcripts/output.json")

  if not out_file.exists():
    dump_transcript(in_file, out_file)

  corpus = assemble_corpus(out_file)
