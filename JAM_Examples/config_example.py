#! env python
__author__ = 'morrj140'

import os
import sys
import ConfigParser
from phase_ALL_Logging import *
logger.setLevel(logging.DEBUG)

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                logger.debug("skip: %s" % option)
        except:
            logger.debug("exception on %s!" % option)
            dict1[option] = None
    return dict1

if __name__ == "__main__":

    Config = ConfigParser.ConfigParser()

    Config.read("as400.cfg")

    logger.debug("%s" % Config.sections())

    Name = ConfigSectionMap("Credential")['name']

    PWD = ConfigSectionMap("Credential")['pwd']


