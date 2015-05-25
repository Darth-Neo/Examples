import os
import sys

from gensim import corpora, models, similarities
from gensim.models import lsimodel

from nl_lib import Logger, Concepts, Tokens
logger = Logger.setupLogging(__name__)

#
# TopicModel to analyze topic concepts via Gensim
#
class TopicsModel(object):
    dictFile       = None
    corpusFile     = None
    lsiFile        = None
    topicsFile     = None
    indexFile      = None
    documentTopics = None

    dictFilename   = "Dictionary.dict"
    corpusFilename = "corpus.mm"
    lsiFilename    = "model.lsi"
    indexFilename  = "topic.index"
    topicsFileneme = "topicsDict.p"

    texts = None

    # Compute similarity between documents / projects
    similarityThreshold = 0.95

    delchars = ''.join(c for c in map(chr, range(255)) if (not c.isalnum() and c != ' '))

    def __init__(self, directory=None, st=None):

        if directory == None:
            directory = os.getcwd() + os.sep

        if st != None:
            self.similarityThreshold = st
            
        self.corpusFile = directory + self.corpusFilename
        self.lsiFile = directory + self.lsiFilename
        self.indexFile = directory + self.indexFilename
        self.dictFile  = directory + self.dictFilename
        self.topicsFile  = directory + self.topicsFileneme

    #def __iter__(self):
    #    for line in open('mycorpus.txt'):
    #        # assume there's one document per line, tokens separated by whitespace
    #        yield dictionary.doc2bow(line.lower().split())

    def saveTopics(self, topics):
        wordConcepts = Concepts.Concepts("TopicConcepts", "Topics")
        for topic in topics:
            for project in topics:
                for word in project:
                    logger.debug("Word:" + word[0])
                    w = wordConcepts.addConceptKeyType(word[0], "Topic")
                    w.count = word[1]
        Concepts.Concepts.saveConcepts(wordConcepts, self.topicsFile)
        return wordConcepts

    def saveDictionary(self):
        if (self.dictionary != None) :
            self.dictionary.save(self.dictFile)

    def loadDictionary(self):
        if (os.path.isfile(self.dictFile)) :
            return corpora.Dictionary.load(self.dictFile)

    def saveCorpus(self):
        if (self.corpus != None) :
            corpora.MmCorpus.serialize(self.corpusFile, self.corpus)

    def loadCorpus(self):
        if (os.path.isfile(self.corpusFile)):
            self.corpus = corpora.MmCorpus(self.corpusFile)
            return self.corpus

    def saveLSI(self):
        self.lsi.save(self.lsiFile)

    def loadLSI(self):
        self.lsi = models.LsiModel.load(self.lsiFile)
        return self.lsi

    def logTexts(self, texts):
        for text in texts:
           logger.info("Text[" + str(texts.index(text)) + "] :  " + text)

    def logTopics(self, topics):
        for topic in topics:
            for word in topic:
                logger.info("Topic[" + str(topic.index(word)) + "] :  " + str(word[0]) + "=" + str(word[1]))

    @staticmethod
    def convertMetric(metric):
        c = metric
        d = float(c)
        return int(d * 100.0)

    def computeTopics(self, texts, nt=50, nw=5):
        self.texts = texts

        # test set
        self.dictionary = corpora.Dictionary(texts)

        # training set
        self.corpus = [self.dictionary.doc2bow(text) for text in texts]

        logger.info("corpus ready")
        for c1 in self.corpus:
            for c2 in c1:
               logger.info("word: %s  count:%s  index:%s" % (self.dictionary[c2[0]], c2[1], c2[0]))

        tfidf = models.TfidfModel(self.corpus)
        logger.info("tfidf: " + str(tfidf))

        corpus_tfidf = tfidf[self.corpus]
        logger.info("corpus_tfidf: " + str(corpus_tfidf))

        # I can print out the topics for LSI
        self.lsi = lsimodel.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=nt)
        logger.info("LSI Complete")
        corpus_lsi = self.lsi[self.corpus]

        logger.info("lsi.print_topics: " + str(self.lsi.print_topics))

        count = 1
        topics = list()
        words = list()

        self.saveLSI()
        self.saveCorpus()
        self.saveDictionary()

        lsiList = self.lsi.print_topics(num_topics=nt, num_words=nw)

        for top in lsiList:
          logger.info("Topic [" + str(lsiList.index(top)) + "] " + str(top))
          words = list()
          for wordcluster in top.split(" +"):
              wc = list()
              wc.append(wordcluster.split("*")[1].lower().strip())
              wc.append(TopicsModel.convertMetric(wordcluster.split("*")[0]))
              words.append(wc)
          topics.append(words)

        return topics

    def computeSimilar(self, j, documentsList, projectList, threshold = 0.98):

        doc = documentsList[j]

        vec_bow = self.dictionary.doc2bow(doc)

        # convert the query to LSI space
        vec_lsi = self.lsi[vec_bow]
        logger.debug("vec_lsi: %s" % (vec_lsi))

        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])
        #self.index.save(self.index)

        # perform a similarity query against the corpus
        sims = self.index[vec_lsi]

        logger.debug("len       : %s" % (sims))
        logger.debug("similarity: %s" % (sims))
        logger.debug("type      : %s" % (type(sims)))
        logger.debug("shape     : %s" % (sims.shape))

        simsList = sims.tolist()
        logger.debug("len       : %s" % (len(simsList)))
        logger.debug("similarity: %s" % (simsList))
        logger.debug("type      : %s" % (type(simsList)))

        projectSimilarity = list()

        for i in range(0, len(simsList)-1):
            if (simsList[i] > threshold) and (projectList[j] != projectList[i])  :
                logger.debug("Project    : %s" % (projectList[j]))
                logger.debug("Topics     : %s" % (documentsList[j]))
                logger.debug("Similar[%s]: %s" % (projectList[i], simsList[i]))
                logger.debug("Topics     : %s" % (documentsList[i]))

                sl = list()
                sl.append(projectList[j])
                sl.append(projectList[i])
                sl.append(str(simsList[i]))
                sl.append(documentsList[j])
                sl.append(documentsList[i])
                projectSimilarity.append(sl)

        logger.debug("Project Similarity List %s" % (projectSimilarity))

        return projectSimilarity

    def loadWords(self, concepts):
        documents = list()
        texts = list()

        wordcount = 0

        # Iterate through the Concepts
        logger.debug("Concept Name:" + concepts.name)

        pc = concepts.getConcepts()
        for p in pc.values():
            logger.debug("Concept: %s" % p.name)

            # Iterate through the Words
            wc = p.getConcepts()
            for w in wc.values():
                logger.debug("Word: %s" % w.name)
                texts.append(w.name)
                wordcount += 1

            documents.append(texts)
            texts = list()

        return documents, wordcount
    
    def loadConceptsWords(self, concepts, delim=" "):
        documents = list()
        texts = list()

        wordcount = 0

        # Iterate through the Concepts
        logger.info("Concept Name:" + concepts.name)

        for document in concepts.getConcepts().values():
            logger.info("Doc: %s" % document.name)

            for sentence in document.getConcepts().values():
                logger.info("sent: %s" % sentence.name)

                for word in sentence.name.split(delim):
                    if len(word) > 1:
                        logger.info("Word: %s" % word)
                        texts.append(word.lower().strip())
                        wordcount += 1

                documents.append(texts)
                texts = list()

        return documents, wordcount
