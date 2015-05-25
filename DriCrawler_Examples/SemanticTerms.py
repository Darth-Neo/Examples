#
# Semantic Term Analysis
#
import os
import csv

from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.TopicCloud import TopicCloud

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.corpus import stopwords

logger = Logger.setupLogging(__name__)

GRAPH = True

if GRAPH == True:
    import pydot
    graph = pydot.Dot(graph_type='graph')
    graph.set_graphviz_executables({'dot': "C:\\Users\\morrj140\\Dev\\graphviz\\bin\\dot.exe",
                                    'twopi': "C:\\Users\\morrj140\\Dev\\graphviz\\bin\\twopi.exe",
                                    'neato': "C:\\Users\\morrj140\\Dev\\graphviz\\bin\\neato.exe",
                                    'circo': "C:\\Users\\morrj140\\Dev\\graphviz\\bin\\circo.exe",
                                    'fdp': "C:\\Users\\morrj140\\Dev\\graphviz\\bin\\fdp.exe"})

    #progs = {'dot': '', 'twopi': '', 'neato': '', 'circo': '', 'fdp': ''}
    

def logChunks(chunks):
    for chunk in chunks:
            logger.info("Chunk %s: .%s." % (chunk.type, chunk)) 
            wordChunk = chunk.string

            for word in chunk.words:
                logger.info("word: .%s." % (word)) 
                synsetsWordNet(word)

def logSentence(sentence):
    logger.info("sentence.string .%s." % sentence.string)             # Tokenized string, without tags.
    logger.info("sentence.words .%s." % sentence.words)               # List of Word objects.
    logger.info("sentence.lemmata .%s." % sentence.lemmata)           # List of word lemmata.
    logger.info("sentence.chunks .%s." % sentence.chunks)             # List of Chunk objects.
    logger.info("sentence.subjects .%s." % sentence.subjects)         # List of NP-SBJ chunks.
    logger.info("sentence.objects .%s." % sentence.objects)           # List of NP-OBJ chunks.
    logger.info("sentence.verbs .%s." % sentence.verbs)               # List of VP chunks.
    logger.info("sentence.relations .%s." % sentence.relations)       # {'SBJ': {1: Chunk('the cat/NP-SBJ-1')},
                                                                    #  'VP': {1: Chunk('sat/VP-1')},
                                                                    #  'OBJ': {}} 
def synsetsWordNet(word):
    s = wordnet.synsets(word)[0]

    logger.info("\tDefinition: %s" % s.gloss)
    logger.info("\t Synonyms : %s" % s.synonyms)
    logger.info("\t Hypernyms: %s" % s.hypernyms())
    logger.info("\t Hyponyms : %s" % s.hyponyms())
    logger.info("\t Holonyms : %s" % s.holonyms())
    logger.info("\t Meronyms : %s" % s.meronyms())
    
def logSemanticTerms (inputFile, outputFile):
    logger.info("Input File: " + inputFile)
    iFile = open(inputFile, "r")

    logger.info("Output File: " + outputFile)
    oFile = open(outputFile , "w")

    writer = csv.writer(oFile)
    reader = csv.reader(iFile)

    wordsConcepts = Concepts("WordsConcepts", "Words")

    NOUN_POS = ['N', 'NN', 'NNP', 'NNS']
    VERB_POS = ['V', 'VD', 'VG', 'VN']
    POS = VERB_POS + NOUN_POS
  
    rownum = 0

    tree = list()

    writer.writerow(["word", "synset.definition", "synset.lemma_names", "synset.examples"])
    
    for row in reader:
        logger.debug("row: %s - %s" % (str(rownum), row))

        # Take first column
        term = row[0]
        
        logger.debug("Term: %s" % term)

        text = nltk.word_tokenize(term)
        
        posTagged = (nltk.pos_tag(text))

        logger.debug("  POS Text: %s" % posTagged)

        for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(term)):
            logger.debug("   Word: " + word + " POS: " + pos)

            if (pos in POS):
                logger.info("Add  POS:" + word)
                wordsConcepts.addConceptKeyType(word, "WORD")
            else:
                logger.info("Skip POS:" + word)

            for synset in wn.synsets(word):

                if GRAPH == True:
                    for i in synset.lemma_names:
                        edge = pydot.Edge(term, i)
                        graph.add_edge(edge)
                    
                writer.writerow([word, synset.definition, synset.lemma_names, synset.examples])

                logger.info("    %s\t%s" % (word, synset.lemma_names))
                #logger.debug("%s\t%s\t%s\t%s" % (word, synset.lemma_names, synset.definition, synset.examples))

                if GRAPH == True:
                    paths = synset.hypernym_paths()

                    prior = None
                    for x in range(0, len(paths)-1):
                        flag = False
                        for synset in paths[x]:
                            if flag == False:
                                prior = synset.name
                                flag = True
                            else:
                                edge = pydot.Edge(prior, synset.name)
                                graph.add_edge(edge)
                                prior = synset.name
                            logger.info("%s" % synset.name)

                    # tie it to the last entry
                    if prior != None:
                        edge = pydot.Edge(prior, term)
                        graph.add_edge(edge)

    iFile.close()
    oFile.close()

    wordsConcepts.logConcepts()
    
    return wordsConcepts
        
if __name__ == "__main__":
    
    # Load Inpit file
    homeDir = os.getcwd()
    
    outputFile = homeDir + os.sep + "SemanticTermsOutput.csv"
    inputFile = homeDir + os.sep + "SemanticTerms_JMB.csv"
    
    #fileList = os.listdir(homeDir + "\\Mega\\")
    #fileList = [
                #'BusinessFunction.csv',
                #'BusinessProcess.csv',
                #'Capability.csv',
                #'Entity.csv',
                #'Functionality.csv',
                #'ITService.csv',
                #'OrganizationalProcess.csv',
                #'Requirements.csv',
                #'SystemProcess.csv'
                #]

    #for f in fileList:
    #    logger.info("File: %s" %f)
    #    inputFile = homeDir + "\\Mega\\" + f
    
    wordsConcepts = logSemanticTerms (inputFile, outputFile)

    Concepts.saveConcepts(wordsConcepts, wordsFile)

    if GRAPH == True:
        graph.write_png('SemanticTerms.png')

        topic = "WORD"
        tc = TopicCloud(wordsConcepts, os.getcwd() + os.sep)

        tc.createCloudImage(topic, size_x=1200, size_y=900, numWords=50, scale=1)

        

    
