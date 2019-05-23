from StackItem import StackItem
import json

class NDictionary(object):
    toRemove = list(("\"", ":", ";", "(", ")", " ", "",'', "DT", "...",'','``',"''"))
    _maxDepth = "mdk"
    _root = "rk"
    def __init__(self, md = 4):
        #self.content = { _maxDepth : md, _root : TreeNode() }
        self.maxDepth = md
        self.root = TreeNode()

    def toJSON(self):
        result = {self._maxDepth: self.maxDepth, self._root : self.root.toJSON()}
        return result

    def fromDict(dict):
        result = NDictionary()
        result.maxDepth = dict[NDictionary._maxDepth]
        result.root = TreeNode.fromDict(dict[NDictionary._root])
        return result

    def toFile(self, path):
        toWrite = self.toJSON()
        file = open(path, "w+")
        file.write(json.dumps(toWrite))
        file.close()

    def fromFile(path):
        file = open(path, "r")
        jsonS = file.read()
        dict = json.loads(jsonS)
        return NDictionary.fromDict(dict)

    def add(self, ngram, annotation):
        self.root.count = self.root.count + 1
        currentNode = self.root
        for i in range(0, len(ngram)):
            tmpNode = None
            if(ngram[i] in currentNode.children):
                tmpNode = currentNode.children[ngram[i]]
                if(not annotation in tmpNode.annotations and annotation is not None):
                    tmpNode.annotations.append(annotation)
            else:
                currentNode.children[ngram[i]] = TreeNode(annotation)
                tmpNode = currentNode.children[ngram[i]]
            currentNode = tmpNode
            currentNode.count = currentNode.count + 1
    
    def addSequence(self, sequence, annotation = None):
        sequence = self.__filter(sequence)
        toAdd = []
        for i in range(0, len(sequence)):
            toAdd.append(sequence[i])
            if(len(toAdd) == self.maxDepth):
                self.add(toAdd, annotation)
                toAdd = toAdd[1:]
        while len(toAdd) > 0:
            self.add(toAdd, annotation)
            toAdd = toAdd[1:]

    def __filter(self, sequence):
        sequence = list(sequence)
        last = None
        nnps = list(("NNP", "NNPS"))
        result = []
        for i in range(0, len(sequence)):
            if(sequence[i] in nnps and last in nnps):
                continue
            if(not (sequence[i] in self.toRemove)):
                result.append(sequence[i])
            last = sequence[i]
        return result
        
    def searchTree(self, init, enterN, exitN, final, **kwargs):
        if init is not None:
            init(kwargs)
        stack = []
        stack.append(StackItem(0, "root", self.root))
        while(len(stack) > 0):
            si = stack.pop()   
            if(si.touched == False):
                if(enterN is not None):
                    enterN(si, kwargs)
                si.touched = True
                stack.append(si)
                for key in si.treeNode.children:
                    stack.append(StackItem(si.depth + 1, key, si.treeNode.children[key]))
            else:
                if(exitN is not None):
                    exitN(si, kwargs)
        if(final is not None):
            return final(kwargs)
        else:
            return

    def print(self, separator = ","):
        _result = "result"
        _separator = "separator"
        dicc = {_separator: separator, _result: ""}
        def enterN(si, kwargs):
            separator = kwargs[_separator]
            result = kwargs[_result]
            result += (si.token + "-" + str(si.treeNode.count) + "-" + str(si.treeNode.annotations) + separator)
            kwargs[_result] = result
        def exitN(si, kwargs):
            separator = kwargs[_separator]
            result = kwargs[_result]
            if(si.depth != 0):
                result += "r" + separator
            else:
                result += "<end>"
            kwargs[_result] = result
        def final(kwargs):
            return kwargs[_result]
        return self.searchTree(None, enterN, exitN, final, **dicc)

    def mostPopular(self, minDepth, maxDepth, howMany = -1):
        _currNGram = "currNGram"
        _counts = "counts"
        _minDepth = "minD"
        _maxDepth = "maxD"
        _howMany = "howMany"
        dicc = {_currNGram: [], _counts: []}
        if(howMany == -1):
            howMany = root.count
        def enterN(si, kwargs):
            counts = kwargs[_counts]
            currNGram = kwargs[_currNGram]
            currNGram.append(si.token)
            candidate = (si.treeNode.count, currNGram.copy(), si.treeNode.annotations)
            if(si.depth in range(minDepth, maxDepth + 1)):
                if(len(counts) < howMany):
                    counts.append(candidate)
                else:
                    counts = sorted(counts, key = lambda x: x[0])
                    if(candidate[0] > counts[0][0]):
                        counts[0] = candidate
            kwargs[_counts] = counts
            kwargs[_currNGram] = currNGram
        def exitN(si, kwargs):
            currNGram = kwargs[_currNGram]
            if(len(currNGram) > 0):
                currNGram = currNGram[0:len(currNGram)-1]
            kwargs[_currNGram] = currNGram
        def final(kwargs):
            counts = kwargs[_counts]
            counts = sorted(counts, reverse = True, key = lambda x: x[0])
            result = ""
            for item in counts:
                result += (str(item[1][1:]) + "-" + str(item[2]) + ": " + str(round(item[0]/self.root.count,5)) + "\n")
            return result
        return self.searchTree(None, enterN, exitN, final, **dicc)

    def fromString(string):
        states = {"token" : 0, "count" : 1, "annon" : 2}
        result = NDictionary()
        stack = []
        stack.aappend(result.root)

        length = len(string)
        iterator = 0

        while(iterator < length):
            next_symbol = string[iterator]





        return result

   


class TreeNode:
    _count = "cn"
    _annotations = "an"
    _children = "ch"
    def __init__(self, annon = None):
        self.count = 0
        if annon is None:
            self.annotations = []
        else:
            self.annotations = [annon]

        self.children = {}
    def toJSON(self):
        result = {self._count: self.count, self._annotations : self.annotations}
        children = {}
        for child in self.children:
            children[child] = self.children[child].toJSON()
        result[self._children] = children
        return result;

    def fromDict(dict):
        result = TreeNode()
        result.count = dict[TreeNode._count]
        result.annotations = dict[TreeNode._annotations]
        childDict = dict[TreeNode._children]
        children = {}
        for child in childDict:
            children[child] = TreeNode.fromDict(childDict[child])
        result.children = children
        return result



