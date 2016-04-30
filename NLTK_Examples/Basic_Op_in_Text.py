#!/usr/bin/env python
from __future__ import division
import os
from nltk.book import *

# lexical richness of the text
def lexical_richness(text):
    return len(set(text)) / len(text)

# percentage of the text is taken up by a specific word
def percentage(word, text):
    return (100 * text.count(word) / len(text))

if __name__ == u"__main__":

    text_choice = u"The Book of Genesis"
    # Enter their names to find out about these texts

    print(u"%s%s " % (os.linesep, text_choice))

    # Length of a text from start to finish, in terms of the words and punctuation symbols that appear.
    print( u"Length of Text: " + str(len(text_choice)))

    # Text is just the set of tokens
    # print sorted(set(text3))
    print(u"Length of Token: " + str(len(set(text_choice))))


    print(u"Lexical richness of the text: %d" + str(lexical_richness(text_choice)))
    print(u"Percentage: " + str(percentage(u"God", text_choice)))
