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


