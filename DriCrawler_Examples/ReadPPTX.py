import openxmllib

doc = openxmllib.openXmlDocument(path="example.pptx")

print ("%s\n" % (doc.coreProperties))

for x in doc.coreProperties:
    print("%s:%s" % (x, doc.coreProperties[x]))

for x in doc.extendedProperties:
    print("%s:%s" % (x, doc.extendedProperties[x]))

print ("%s\n" % (doc.indexableText(include_properties=True)))
