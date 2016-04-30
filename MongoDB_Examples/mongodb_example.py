#!/usr/bin/env python
# __author__ = "james.morris"
import datetime
from pymongo import MongoClient

from Logger import *

logger = setupLogging(__name__)
logger.setLevel(INFO)

if __name__ == u"__main__":
    client = MongoClient(u"localhost", 27017)

    if False:
        # client = MongoClient("mongodb://localhost:27017/")
        # db = client["test-database"]
        db = client[u"stackoverflow"]

        # collection = db.test_collection
        # collection = db["test-collection"]
        collection = db[u"questions"]

        post = {u"author": u"Mike", u"text": u"My first blog post!", u"tags": [u"mongodb", u"python", u"pymongo"],
                u"date": datetime.datetime.utcnow()}

        posts = db.posts

        post_id = posts.insert_one(post).inserted_id

        logger.info(u"post_id : %s " % post_id)

    c = db.collection_names(include_system_collections=False)

    logger.info(u"c - %s" % c)

    # p = posts.find_one()
    p = posts.find()

    logger.info(u"p - %d %s[%s]" % (p.count(), p, type(p)))

    for x in p:
        logger.info(u"%s[%s]" % (x, x))
