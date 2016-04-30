#!/usr/bin/env python
__author__ = u"james.morris"
from nltk.corpus import genesis
from nltk.text import Text

if __name__ == u"__main__":
    # names of the Text
    text = Text(genesis.words('english-kjv.txt'), name="The Book of Genesis")
    print text

    # count the word in the Text
    print "===Count==="
    print text.count("Adam")

    # 'concordance()' view shows us every occurrence of a given word, together with some context.
    # Here 'Adam' search in 'The Book of Genesis'
    print "===Concordance==="
    print text.concordance("Adam")

    # Appending the term similar to the name of the text
    print "===Similar==="
    print text.similar("Adam")

    # Contexts are shared by two or more words
    print "===Common Contexts==="
    text.common_contexts(["Adam", "Noah"])

    print "===Dispersion Plotr==="
    text.dispersion_plot(["God","Adam", "Eve", "Noah", "Abram","Sarah", "Joseph", "Shem", "Isaac"])
