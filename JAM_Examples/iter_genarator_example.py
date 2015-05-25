#
# iter / generator Shell
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'
import os
import sys
import pickle
from py2neo import neo4j
from py2neo.neo4j import BatchRequestList

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import ConceptGraph

#
# Script to reset Neo4J
#
resetNeo4J = u"/Users/morrj140/Development/neo4j2/bin/reset.sh"

def crawl(directory):
    n = 0
    for root, dirs, files in os.walk(directory, topdown=True):
        for name in files:
            n += 1
            nameFile = os.path.join(root, name)
            logger.debug(u"%d - %s" % (n, nameFile))

            if nameFile[-9:] <> u".DS_Store":
                fullPath = directory + nameFile[1:]
                nl = loadList(fullPath)
                yield fullPath, nl


def loadList(listFile):
    nl = None

    if not os.path.exists(listFile):
        logger.error(u"%s : Does Not Exist!" % listFile)

    try:
        cf = open(listFile, u"rb")
        nl = pickle.load(cf)
        logger.info(u"Loaded : %s" % (listFile))
        cf.close()
    except:
        logger.error(str(sys.exc_info()[0]))

    return nl[0]

def convertConcepts(nl):

    ni = iter(nl)
    e = next(ni)

    concepts = Concepts(e[0], u"Library")
    d = concepts.addConceptKeyType(e[1], u"Table")

    while e <> None:
        logger.info(u"e : %s" % e)
        f = d.addConceptKeyType(e[2], u"Column")
        f.properties[u"Description"] = e[3]

        try:
            e = next(ni)
        except StopIteration:
            break

def convertLibraryTablesToDict(listFile):

    listLibraryTable = loadList(listFile)

    dictLibraryTables = dict()

    for x in listLibraryTable:
        lt = u"%s.%s" % ([0], x[1])
        logger.info(u"Table : %s \t %s " % (lt, x[2]))
        dictLibraryTables[lt] = x[2]

    return dictLibraryTables

if __name__ == u"__main__":

    dirStart= u"." + os.sep + u"../data"

    listFile = u"../LibraryTables.p"

    dictLibraryTables = convertLibraryTablesToDict(listFile)

    gdb  = u"http://localhost:7574/db/data/"

    dc = crawl(dirStart)
    fullPath, nl = dc.next()

    while nl != None:
        try:
            logger.info(u"%s : %d[%20s]" % (fullPath, len(nl), nl))
            fullPath, nl = dc.next()

        except StopIteration:
            pass

