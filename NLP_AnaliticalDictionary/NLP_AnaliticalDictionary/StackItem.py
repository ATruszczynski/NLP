class StackItem:
    def __init__(self, d, t, tn):
        self.touched = False
        self.depth = d
        self.token = t
        self.treeNode = tn

class NGramTuple:
    def __init__(self, _ngram, _value):
        self.ngram = _ngram
        self.value = _value
    def __str__(self):
        return "<" + str(self.ngram) + ", " + str(self.value) + ">"

class ResultTuple:
    def __init__(self, _answer, _source, _reasoning = []):
        self.answer = _answer
        self.source = _source
        self.score = 0
        self.reasoning = _reasoning
        self.dealbreaker = 1
    def print(self):
        return "[" + self.answer + ", " + self.source + ", " + str(self.score) + ", " + str(self.reasoning) + ", " + str(self.dealbreaker) + "]"
    def __str__(self):
        return self.print()
        


