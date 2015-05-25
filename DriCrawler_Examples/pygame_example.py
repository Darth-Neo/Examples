from TagCloud import TagCloud

t = TagCloud()
words = [{"text": "coffee", "weight": 20296.0},{"text": "love", "weight": 15320.0}]
print t.draw(words)