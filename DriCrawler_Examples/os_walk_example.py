import os

rootDir = "C:\\Users\\morrj140\\Documents\\System Architecture\\Accovia"

def searchSubDir(rootdir):
    print("SubDir : %s" % rootdir)
    
    for root, dirs, files in os.walk(rootDir, topdown=False):
        for name in files:
            print("--%s" % (os.path.join(root, name)))
            
        for directory in dirs:
            #print("subdir : %s" % os.path.join(root, directory))
            pass
        
if __name__ == '__main__': 
    searchSubDir(rootDir)
