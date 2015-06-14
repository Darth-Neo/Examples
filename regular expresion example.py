from pattern.web    import Bing, Google, plaintext
from pattern.en     import parsetree
from pattern.search import search, match
from pattern.graph  import Graph
import re
import logging

# create logger
logger = logging.getLogger(__name__)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.setLevel(logging.INFO)

s = 'this is a protocol to induce disseminated candidiasis in mice'
Sentence = 'candida albicans/NNS/I-NP/O infection/NN/I-NP/O experiments/NNS/I-NP/O were/VBD/B-VP/O performed/VBN/I-VP/O as/IN/B-PP/O previously/RB/B-VP/O described/VBN/I-VP/O with/IN/B-PP/B-PNP minor/JJ/B-NP/I-PNP modifications/NNS/I-NP/I-PNP .../:/O/O'
logger.info(s)

s = plaintext(s)
logger.info(s)

s = parsetree(s)
logger.info(s)

#p = r'^*(V?)* \s\w*\s(NN?)*'
p = r'(NN)+ (VB)+'
for m in search(p, s):
    logger.info(str(m))
