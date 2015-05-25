#!/usr/bin/python
#
# Natural Language Processing of Information
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicsModel import TopicsModel

class DocumentsSimilarity(object):
    concepts = None
    conceptsSimilarity = None
    tm = None
    documentsList = None
    wordcount = None
    threads = None

    conceptsFile = "words.p"
    conceptsSimilarityFile = "documentsSimilarity.p"

    # Compute similarity between documents / concepts
    similarityThreshold = 0.95
    num_topics = 20

    def __init__(self, similarityThreshold=0.95, num_topics=100):
        logger.info("Load Concepts from " + self.conceptsFile)
        self.concepts = Concepts.loadConcepts(self.conceptsFile)
        
        logger.info("Loaded Concepts")

        self.similarityThreshold = similarityThreshold
        self.num_topics = num_topics

        self.conceptsSimilarity = Concepts("ConceptsSimilarity", "Similarities")

        self.conceptsList = list()

    def createTopics(self):
        if len(self.concepts.getConcepts()) > 2:
            self.computeTopics()
            self.computeSimilarity()
        else:
            logger.warn("Not enough concepts to compare.")
            
    def computeTopics(self):
        self.tm = TopicsModel()

        logger.info("Load Documents from Concepts")
        self.documentsList, self.wordcount = self.tm.loadConceptsWords(self.concepts)

        logger.info("Read " + str(len(self.documentsList)) + " Documents, with " + str(self.wordcount) + " words.")

        logger.info("Compute Topics")
        topics = self.tm.computeTopics(self.documentsList, nt=self.num_topics)

        logger.info("Compute Topics")
        self.tm.logTopics(topics)

        logger.info("Saving Topics")
        topicsConcepts = self.tm.saveTopics(topics)

    def computeSimilarity(self):
        logger.info("Compute Similarity")

        # Caution: if typeName is not correct this fails!
        self.conceptsList = [x for x in self.concepts.dictChildrenType("Document").keys()]

        for j in self.documentsList:
            indexNum = self.documentsList.index(j)
            logger.info("conceptsList[" + str(indexNum) + "]=" + str(self.conceptsList[indexNum]))
            logger.debug("documentsList[" + str(indexNum) + "]=" + str(j))

            self.doComputation(j, self.similarityThreshold, self.conceptsList)

        self.conceptsSimilarity.logConcepts()

        Concepts.saveConcepts(self.conceptsSimilarity, conceptsSimilarityFile)

        logger.info("Complete createTopics")

    def doComputation(self, j, similarityThreshold, conceptsList):
        
        pl = self.tm.computeSimilar(self.documentsList.index(j), self.documentsList, conceptsList, similarityThreshold)

        if len(pl) != 0:
            logger.debug("   similarity above threshold")
            logger.debug("pl:" + str(pl))

            for l in pl:
                logger.info("l:" + str(l))
                ps = self.conceptsSimilarity.addConceptKeyType(l[0], "Similar")
                ps.count = TopicsModel.TopicsModel.convertMetric(l[2])
                #rt1 = ps.addConceptKeyType(str(l[3]), "SimilarTopics")
                #rt1 = len(l[3])
                pt = ps.addConceptKeyType(l[1], "Concept")
                #rt2 = pt.addConceptKeyType(str(l[4]), "ProjectTopics")
                #rt2.count = len(l[4])
                common = set(l[3]) & set(l[4])
                lc = [x for x in common]
                for x in common:
                    pc = pt.addConceptKeyType(x, "CommonTopic")
                    pc.count = len(lc)
                
        else:
            logger.debug("   similarity below threshold")

if __name__ == "__main__":
    ds = DocumentsSimilarity()
    ds.computeTopics()
    ds.computeSimilarity()


