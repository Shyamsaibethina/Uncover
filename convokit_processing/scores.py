import json
import pandas as pd
try:
    import convokit_processing.conversation as conversation
except:
    import conversation
from pathlib import Path

import pandas as pd
from convokit import (Coordination, Corpus, PolitenessStrategies, Speaker,
                      TextParser, Utterance, download)

import convokit_processing.conversation as conversation


def main():
    corpus = Corpus(filename="convokit_processing/test_corpus/")
    utt = corpus.get_utterance("1.Pink.1")
    print("RAW TEXT:" + utt.text + "\n")
    print("Sentences: ")
    for i, x in enumerate(utt.meta["parsed"]):
        stra = ""
        for y in x["toks"]:
            stra += " " + y["tok"]

        print(str(i) + " " + stra[:50] + "...")

    print()
    for ((k, v), (k1, v2)) in zip(
        utt.meta["politeness_strategies"].items(),
        utt.meta["politeness_markers"].items(),
    ):
        # print(k,v,k1,v2)
        print(k[21 : len(k) - 2] + " results:")
        print("Markers: " + str(v2) + "\n")


def speech_transcript_to_corpus(filename):
    output = Path("output.json")
    with output.open() as file:
        df = pd.DataFrame(json.load(file))
        print(df)


def getPolitenessScores(corpus, uid):
    ps = PolitenessStrategies()
    data = ps.summarize(corpus, lambda utt: utt.speaker.id == uid)
    politeness = data["feature_politeness_==HASPOSITIVE=="] - data["feature_politeness_==HASNEGATIVE=="]
    data._set_value("politeness", politeness)
    return data #politeness

def getCoordinationScore(corpus, speakerid, targetid=None):
    coord = Coordination()
    coord.fit(corpus)
    if targetid == None:
        data = coord.summarize(
            corpus,
            lambda speaker: speaker.id == speakerid,
            focus="speakers",
            summary_report=True,
        )
    else:
        data = coord.summarize(
            corpus,
            lambda speaker: speaker.id == speakerid,
            lambda speaker: speaker.id == targetid,
            summary_report=True,
        )

    if data["agg1"] is None:
        data["agg1"] = 0
    if data["agg2"] is None:
        data["agg2"] = 0
    if data["agg3"] is None:
        data["agg3"] = 0

    coordination = (data["agg1"] + data["agg2"] + data["agg3"]) / 3
    return coordination


def processCorpus(corpus):
    parser = TextParser(verbosity=1000)
    corpus = parser.transform(corpus)
    ps = PolitenessStrategies()
    coord = Coordination()
    corpus = ps.transform(corpus, markers=True)
    corpus = coord.fit_transform(corpus)
    return corpus

def get_scores_from_audio(filename: Path, name1="1", name2="2"):
    #conversation.dump_transcript(filename, Path("convokit/transcripts/output.json"))
    corpus = conversation.assemble_corpus(Path("convokit_processing/transcripts/output.json"))
    corpus = processCorpus(corpus)
    pscore1 = getPolitenessScores(corpus, "1")
    pscore2 = getPolitenessScores(corpus, "2")
    pscore1.name = name1
    pscore2.name = name2
    cscore1 = getCoordinationScore(corpus, "1", "2")
    cscore2 = getCoordinationScore(corpus, "2", "1")
    pscore1._set_value("coordination", cscore1)
    pscore2._set_value("coordination", cscore2)
    scores = pscore1.to_frame().join(pscore2)
    return scores


if __name__ == "__main__":
    scores = get_scores_from_audio(Path("convokit_processing/audio/long.wav"))
    print(scores)
