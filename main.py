from convokit import Corpus, Speaker, Utterance
from convokit import download
from convokit import TextParser

corpus = Corpus(download('gap-corpus'))

parser = TextParser(verbosity=1000)
corpus = parser.transform(corpus)
