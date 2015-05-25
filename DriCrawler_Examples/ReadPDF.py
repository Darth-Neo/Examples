# Crawl a directory for documents and pull out the text
import sys
import os
import csv
import glob

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from pyPdf import PdfFileReader

def getPDFText(filename):
        logger.info("filename: %s" % filename)
        newparatextlist = []

        pdfDoc = PdfFileReader(file(filename, "rb"))
        
        pdfDict = pdfDoc.getDocumentInfo()
        c = Concepts(filename, "PDF")
        for x in pdfDict.keys():
	    try:
                c.addConceptKeyType(x[1:], pdfDict[x])
            except:
                logger.warn("ops...")
 
        #c.logConcepts()
        
        for page in pdfDoc.pages:
            text = page.extractText()
            logger.info("PDF : %s" % text)
            newparatextlist.append(text + ". ")

        return newparatextlist

if __name__ == '__main__':
	text = getPDFText("./example.pdf")


