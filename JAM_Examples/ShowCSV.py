#! env python
__author__ = 'morrj140'

import csv
import sys
import pickle

from phase_ALL_Logging import *
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":

    listTables = list()

    with open('export.csv', 'rU') as csvfile:

        csvFile = csv.reader(csvfile, delimiter=',')

        for row in csvFile:
            print("row : %s" % row)

            for col in row:
                if len(col) == 4:
                    bo  = row[0].strip()
                    tb  = row[1].strip()
                    do  = row[2].strip()
                    to   = row[3].strip()

                    print("%s - %s.%s" % (bo, do, to))

                    nl = list()
                    nl.append(bo)
                    nl.append(do)
                    nl.append(to)

                    listTables.append(nl)

    cf = open("bo_do_to.p", "wb")
    pickle.dump(listTables, cf)
    cf.close()