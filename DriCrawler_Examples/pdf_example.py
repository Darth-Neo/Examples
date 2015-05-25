
import os
import glob
from pyPdf import PdfFileReader

if __name__ == "__main__":

    pdfFile = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\2013Oct21 DLP ICE update gbts wdpro v2.pdf"

    input = PdfFileReader(file(pdfFile, "rb"))
    for page in input.pages:
        print page.extractText()

    
