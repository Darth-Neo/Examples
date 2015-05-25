__author__ = 'morrj140'

from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

try:
    import textract
except:
    pass

if u'textract' in dir():


    TEXTRACT = True
    logger.info(u"Using textract parser")

    logger.info(u"PDF ...")
    text = textract.process(u'./examples/example.pdf')
    logger.info(text[0:20])

    logger.info(u"PPTX ...")
    text = textract.process(u'./examples/example.pptx')
    logger.info(text[0:20])

    logger.info(u"XLSX ...")
    text = textract.process(u'./examples/example.xlsx')
    logger.info(text[0:20])

    logger.info(u"DOCX ...")
    text = textract.process(u'./examples/example.docx')
    logger.info(text[0:20])

    logger.info(u"txt ...")
    text = textract.process(u'./examples/example.txt')
    logger.info(text[0:20])

    if False:
        logger.info(u"jpg ...")
        text = textract.process(u'./examples/example.jpg')
        logger.info(text[0:20])

        logger.info(u"png ...")
        text = textract.process(u'./examples/example.png')
        logger.info(text[0:20])