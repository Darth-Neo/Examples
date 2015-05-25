import logging
from scipy.odr import models
from sklearn import metrics
import unittest
import os
import os.path
import tempfile

import numpy
from matplotlib.pyplot import plot, show
from sklearn.cluster import KMeans
from gensim.matutils import corpus2dense
import gensim
import logging

from gensim.corpora import mmcorpus, Dictionary
from gensim.models import lsimodel, ldamodel, tfidfmodel, rpmodel, logentropy_model, TfidfModel, LsiModel
from gensim import matutils,corpora

from scipy.cluster.vq import kmeans,vq

test_data_dir  = "/home/vinayb/data/reuters-21578-subset-4315"
#test_data_dir  = "/home/vinayb/data/reuters-21578-example"
#test_data_dir  = "/home/vinayb/data/junk"
#test_data_dir  = "/home/vinayb/data/20news/20news-bydate-test"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            #print file
            document = open(os.path.join(root, file)).read() # read the entire document, as one big string
            yield gensim.utils.tokenize(document, lower=True) # or whatever tokenization suits you

class MyCorpus(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        self.dictionary.filter_extremes(no_below=1, keep_n=30000) # check API docs for pruning params

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)

corpus = MyCorpus(test_data_dir) # create a dictionary
for vector in corpus: # convert each document to a bag-of-word vector
    print vector

topics = 200
num_clusters = 4

print "Create models"
lsi_model = LsiModel(corpus, id2word=corpus.dictionary, num_topics=topics)
corpus_lsi = lsi_model[corpus]

print "Done creating models"


#lsi_model_2 .print_topics(5)

topic_id = 0
for topic in lsi_model.show_topics(num_words=5):
    print "TOPIC (LSI2) " + str(topic_id) + " : " + topic
    topic_id+=1


#for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
#    print "Doc " + str(doc)


corpus_lsi_dense = corpus2dense(corpus_lsi, topics)
print "Dense Matrix Shape " + str(corpus_lsi_dense.shape)


#attempt scikit integration
km = KMeans(k=num_clusters, init='random', max_iter=100, n_init=1, verbose=1)
km.fit(corpus_lsi_dense)


#attempt scipy integration
# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(corpus_lsi_dense,2)
# assign each sample to a cluster
idx,_ = vq(corpus_lsi_dense,centroids)

# some plotting using numpy's logical indexing
plot(
    corpus_lsi_dense[idx==0,0],corpus_lsi_dense[idx==0,1],'ob',
    corpus_lsi_dense[idx==1,0],corpus_lsi_dense[idx==1,1],'or',
    corpus_lsi_dense[idx==2,0],corpus_lsi_dense[idx==2,1],'og',
    corpus_lsi_dense[idx==3,0],corpus_lsi_dense[idx==3,1],'xr'
)

plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()

##print str(km.labels_)
#labels = km.labels_      #<============WRONG
#print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_)
#print "Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_)
#print "V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_)
#print "Adjusted Rand-Index: %.3f" %\
#      metrics.adjusted_rand_score(labels, km.labels_)
#print "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(
#    corpus_lsi_dense, labels, sample_size=1000)
#
#print
