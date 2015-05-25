#! env jython
__author__ = 'morrj140'

import os
import sys
import ConfigParser

from javax.swing import JFrame, JButton
from java.awt import Color
from com.ibm.as400.access import AS400JDBCDriver
from java.sql import DriverManager

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

#
# Load configuration values
#
Config = ConfigParser.ConfigParser()
Config.read("as400.cfg")
name = ConfigSectionMap("Credential")['name']
pwd = ConfigSectionMap("Credential")['pwd']

#logger.debug("%s[%s]" % (name, pwd))

def change_text(event):

        lq1 = "SYSIBM"
        aq1 = "%s.SQLSCHEMAS" % lq1
        aq2 = "%s.SQLTABLES" % lq1
        aq3 = "%s.SQLCOLUMNS" % lq1

        aq4 = "select * from qsys2/systables select * from qsys2/syscolumns select * from qsys2/sysindexes"

        DriverManager.registerDriver(AS400JDBCDriver())
        logger.debug("Connecting...")

        server = "AS400XO.noceast.dws.disney.com"
        lq2 = "DVDSFIL"
        tq1 = "%s.CTCMPF" % lq2

        con = DriverManager.getConnection("jdbc:as400://%s/apilib;naming=sql;errors=full;date format=iso;extended dynamic=true;package=JDBCExa;package library=apilib" % server,
                                           name, pwd)

        logger.debug("Established Connection with: %s" % server)

        query = "SELECT TABLE_NAME, TABLE_TEXT FROM %s where TABLE_SCHEM = '%s'" % (aq2, lq2)

        #query = "SELECT COLUMN_NAME, COLUMN_TEXT, TYPE_NAME FROM %s where TABLE_SCHEM = '%s'" % (aq3, lq2)

        logger.debug("Query: %s" % query)

        stmnt = con.prepareStatement(query)

        results = stmnt.executeQuery()

        i = 0
        while results.next():
            i += 1
            #logger.debug("%s" % results)

            logger.debug("%s : %s" % (results.getString("TABLE_NAME"), results.getString("TABLE_TEXT")))

            #logger.debug("%s : %s [%s]" % (results.getString("COLUMN_NAME"), results.getString("COLUMN_TEXT"), results.getString("TYPE_NAME")))

            if i == 1000:
                exit()

        logger.debug("Success!")

def exit_all(event):
    exit

if __name__ == "__main__":
    f = JFrame('Hello, Jython!', defaultCloseOperation = JFrame.EXIT_ON_CLOSE, size = (550, 200))

    f.setResizable(True)

    b = JButton('Connect!', actionPerformed=change_text)
    #d = JButton('Exit!!', actionPerformed=exit_all)

    c = f.getContentPane()
    c.setBackground(Color.DARK_GRAY)
    c.add(b)
    #c.add(d)

    f.setVisible(True)
