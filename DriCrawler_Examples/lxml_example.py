
#!/usr/bin/python
#
# Archimate to Concepts
#
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

def print_xml(el, i=3, n=0):
    if i==0:
        return

    spaces = " " * n
    n = n + 1

    #print("%se.%d.%s - %s" % (spaces, i, el.tag, el.text))
    print("%se.%d.%s" % (spaces, i, el.tag))

    spaces = " " * n
    n = n + 1

    #nm = el.nsmap
    #for n in nm:
    #    print("--%s = %s" % (n, nm[n]))

    attributes = el.attrib
    for atr in attributes:
        print("%sa.%d.%s = %s" % (spaces, i, atr, attributes[atr]))

    i = i - 1
    for elm in el:
        print_xml(elm, i, n)

def print_folders(tree):
    r = tree.getroot()

    r = tree.xpath('folder')

    for x in r:
        print("%s" % (x.get("name")))

def print_folder(tree, folder):

    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        print_xml(x, i=6)

def print_elements(tree):
    r = tree.getroot()

    r = tree.xpath('folder/element')

    for x in r:
        print x.get("name")

def print_id(tree, id):
    a = "id"
    p = "//child[@%s=\"%s\"]" % (a, id)
    r = tree.xpath("//@id=\"%s\"" % id, namespaces=namespaces)

    try:
        print_xml(r[0], i=1)
    except:
        print("Fail - %s" % p)

def print_types(tree, a):

    dictTypes = dict()

    r = tree.xpath("//@%s" % a, namespaces=namespaces)

    for x in r:
        if dictTypes.has_key(x):
            dictTypes[x] += 1
        else:
            dictTypes[x] = 1

    for x in dictTypes:
        #print("%s=%d" % (x,dictTypes[x]))
        print("Parent - %s:ID - %s" % (x.getparent().get("name"),x.getparent().get("id")))

        p = "//element[@%s=\"%s\"]" % (a, x)
        r = tree.xpath(p, namespaces=namespaces)

        if len(r) > 0:
            print_xml(r[0], i=1)

if __name__ == "__main__":

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/DNX Phase 2/DNX Phase 2 0.8.archimate"

    print("Using : %s" % fileArchimate)

    #tree = etree.parse("archi.xml")

    tree = etree.parse(fileArchimate)

    #print_folders(tree)

    #print_types(tree, "xsi:type")

    #print_folder(tree, "Business")
    #print_folder(tree, "Application")
    #print_folder(tree, "Technology")
    #print_folder(tree, "Motivation")
    #print_folder(tree, "Implementation & Migration")
    #print_folder(tree, "Connectors")
    #print_folder(tree, "Relations")
    #print_folder(tree, "Views")

    #print_elements(tree)

    for element in tree.getroot():
        print_xml(element, i=3)


