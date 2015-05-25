__author__ = u'morrj140'
import os
import sys

from phase_ALL_Logging import *
logger.setLevel(logging.INFO)

if __name__ == u"__main__":

    logger.info(u"Number of arguments: %d" % len(sys.argv))
    logger.info(u"Argument List: %s" % str(sys.argv))

    logger.info(u"Argument[0]: %s" % sys.argv[0])
    logger.info(u"Argument[1]: %s" % sys.argv[1])