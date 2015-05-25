import openxmllib
doc = openxmllib.openXmlDocument(path=‘example.xlsx')
print doc.coreProperties
print doc.extendedProperties
print doc.indexableText(include_properties=True)
