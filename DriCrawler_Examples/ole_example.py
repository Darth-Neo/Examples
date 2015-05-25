import OleFileIO_PL

oleFile = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Introduction to GBTS - v1.1.pptx"

# Test if a file is an OLE container:
assert OleFileIO_PL.isOleFile(oleFile)

# Open an OLE file:
ole = OleFileIO_PL.OleFileIO(oleFile)

# Get list of streams:
print ole.listdir()

# Test if known streams/storages exist:
if ole.exists('worddocument'):
    print "This is a Word document."
    print "size :", ole.get_size('worddocument')
    if ole.exists('macros/vba'):
         print "This document seems to contain VBA macros."

# Extract the "Pictures" stream from a PPT file:
if ole.exists('Pictures'):
    pics = ole.openstream('Pictures')
    data = pics.read()
    f = open('Pictures.bin', 'w')
    f.write(data)
    f.close()

# Extract metadata (new in v0.24) - see source code for all attributes: meta = ole.get_metadata()
print 'Author:', meta.author
print 'Title:', meta.title
print 'Creation date:', meta.create_time
# print all metadata:
meta.dump()

# Close the OLE file: ole.close()

# Work with a file-like object (e.g. StringIO) instead of a file on disk: data = open('myfile.doc', 'rb').read()
f = StringIO.StringIO(data)
ole = OleFileIO_PL.OleFileIO(f)
print ole.listdir()
ole.close()
