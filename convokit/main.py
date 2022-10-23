from audioop import avg
from convokit import Corpus, Speaker, Utterance
from convokit import download
from convokit import TextParser
from convokit import PolitenessStrategies, Coordination
import json
import pandas as pd
from pathlib import Path


def main():
    corpus = Corpus(filename="convokit/test_corpus/")
    utt = corpus.get_utterance('1.Pink.1')
    print("RAW TEXT:" + utt.text + "\n")
    print("Sentences: ")
    for i, x in enumerate(utt.meta["parsed"]):
        stra = ""
        for y in x["toks"]:
            stra += " " + y["tok"]
    
        print(str(i) + " " + stra[:50] + "...") 

    print()
    for ((k,v),(k1,v2)) in zip(utt.meta["politeness_strategies"].items(),utt.meta["politeness_markers"].items()):
        #print(k,v,k1,v2)
        print(k[21:len(k)-2] + " results:")
        print("Markers: " + str(v2) + "\n")

def speech_transcript_to_corpus(filename):
    # with open(filename) as f:
    #     data = json.load(f)
    #     words = data["response"]["results"][0]["alternatives"][0]["words"] 

    # utterances = []
    # for x in words:
    #     utterance = {"id":x["speakerTag"]+x["startTime"], "speaker":x["speakerTag"], "text":x["word"], "timestamp":x["startTime"], "reply-to":None, "vectors":None}
    #     utterances.append(utterance)
    
    # df = pd.DataFrame.from_records(utterances)
    # print(df)
    # corpus = Corpus.from_pandas(df)

    output = Path('output.json')
    with output.open() as file:
        df = pd.DataFrame(json.load(file))
        print(df)

def getPolitenessScores(corpus, uid):
    ps = PolitenessStrategies()
    data = ps.summarize(corpus, lambda utt: utt.speaker.id == uid)
    politeness = data["feature_politeness_==HASPOSITIVE=="] - data["feature_politeness_==HASNEGATIVE=="]
    return data #politeness

def getCoordinationScore(corpus, speakerid, targetid=None):
    coord = Coordination()
    coord.fit(corpus)
    if targetid == None:
        data = coord.summarize(corpus, lambda speaker: speaker.id == speakerid, focus="speakers", summary_report=True)
    else:
        data = coord.summarize(corpus, lambda speaker: speaker.id == speakerid, lambda speaker: speaker.id == targetid, summary_report=True)

    if data["agg1"] is None:
        data["agg1"] = 0
    if data["agg2"] is None:
        data["agg2"] = 0
    if data["agg3"] is None:
        data["agg3"] = 0

    coordination = (data["agg1"] + data["agg2"] + data["agg3"]) / 3
    return coordination

def processCorpus(corpus):
    ps = PolitenessStrategies()
    coord = Coordination()
    corpus = ps.transform(corpus)
    corpus = coord.fit_transform(corpus)
    return corpus

if __name__ == "__main__":
    corpus = Corpus("convokit/test_corpus")
    pscore= getPolitenessScores(corpus, "1.Pink")
    cscore = getCoordinationScore(corpus, "1.Blue", "1.Pink")
    print(pscore, cscore)