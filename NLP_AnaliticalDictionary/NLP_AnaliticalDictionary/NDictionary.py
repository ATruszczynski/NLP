from StackItem import StackItem
import nltk
import docx2txt
#from NDictionary import *
import sys
import json
import os
import ntpath

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

    def toFile(self, path):
        toWrite = self.toJSON()
        file = open(path, "w+")
        file.write(json.dumps(toWrite))
        file.close()

    def fromJSONFile(path):
        file = open(path, "r")
        jsonS = file.read()
        file.close()
        dict = json.loads(jsonS)
        return NDictionary.fromDict(dict)

    def fromTxtFile(path, treeDep):
        file = open(path, "r")
        text = file.read()
        file.close()

        tree = NDictionary(treeDep)
        tree.addSequence(txtToPOS(text))
        return tree

    def add(self, ngram, annotation):
        
        currentNode = self.root
        for i in range(0, len(ngram)): #przechodzimy po ścieżce w drzewie definiowanej przez ciąg POS-tagów
            self.root.count = self.root.count + 1
            if(annotation is not None):
                if not annotation in self.root.annotations:
                    self.root.annotations[annotation] = 0
                self.root.annotations[annotation] = self.root.annotations[annotation] + 1
            tmpNode = None
            if(ngram[i] in currentNode.children): #element jest dzieckiem danego węzła
                tmpNode = currentNode.children[ngram[i]]
                if(not annotation in tmpNode.annotations and annotation is not None):
                   tmpNode.annotations[annotation] = 0
            else:
                currentNode.children[ngram[i]] = TreeNode(annotation)
                tmpNode = currentNode.children[ngram[i]]
            currentNode = tmpNode
            currentNode.count = currentNode.count + 1
            if annotation is not None:
                currentNode.annotations[annotation] = currentNode.annotations[annotation] + 1
        
    


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
        currNGram = []
        stack.append(StackItem(0, "root", self.root))
        while(len(stack) > 0):
            si = stack.pop()  
            if(si.touched == False):
                currNGram.append(si.token)
                if(enterN is not None):
                    enterN(si, currNGram, kwargs)
                si.touched = True
                stack.append(si)
                for key in si.treeNode.children:
                    stack.append(StackItem(si.depth + 1, key, si.treeNode.children[key]))
            else:
                if(exitN is not None):
                    exitN(si, currNGram, kwargs)
                currNGram.pop()
        if(final is not None):
            return final(kwargs)
        else:
            return

    def print(self, separator = ","):
        _result = "result"
        _separator = "separator"
        dicc = {_separator: separator, _result: ""}
        def enterN(si, currNGram, kwargs):
            separator = kwargs[_separator]
            result = kwargs[_result]
            result += (si.token + "-" + str(si.treeNode.count) + "-" + str(si.treeNode.annotations) + separator)
            kwargs[_result] = result
        def exitN(si, currNGram, kwargs):
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
        _counts = "counts"
        dicc = {_counts: []}
        if(howMany == -1):
            howMany = self.root.count
        def enterN(si, currNGram, kwargs):
            counts = kwargs[_counts]
            candidate = (si.treeNode.count, currNGram.copy(), si.treeNode.annotations)
            if(si.depth in range(minDepth, maxDepth + 1)):
                if(len(counts) < howMany):
                    counts.append(candidate)
                else:
                    counts = sorted(counts, key = lambda x: x[0])
                    if(candidate[0] > counts[0][0]):
                        counts[0] = candidate
            kwargs[_counts] = counts
        def final(kwargs):
            counts = kwargs[_counts]
            counts = sorted(counts, reverse = True, key = lambda x: x[0])
            result = ""
            for item in counts:
                result += (str(item[1][1:]) + "-" + str(item[2]) + ": " + str(round(item[0]/self.root.count,5)) + "\n")
            return result
        return self.searchTree(None, enterN, None, final, **dicc)

    def HTTicks(tree, hyperTree):
        _currTick = "currTicks"
        dicc = { _currTick: {} }
        def enterN(si, currNGram, kwargs):
            currTicks = kwargs[_currTick]

            htnode = hyperTree.access(currNGram)
            if htnode is not None:
                for ann in htnode.annotations:
                    if not ann in currTicks:
                        currTicks[ann] = 0
                    currTicks[ann] = currTicks[ann] + htnode.annotations[ann]

            kwargs[_currTick] = currTicks
        
        def final(kwargs):
            currTicks = kwargs[_currTick]
            for i in currTicks:
                currTicks[i] = currTicks[i] / hyperTree.root.annotations[i]
            ct_sort_keys = sorted(currTicks, key=currTicks.get, reverse=True)

            result = {}
            for r in ct_sort_keys:
                result[r] = currTicks[r]
            return result
        return tree.searchTree(None, enterN, None, final, **dicc)

    def treeDistance(tree1, tree2, metric):
        _distance = "distance"
        dicc = { _distance: 0 }
        def enterN(si, currNGram, kwargs):
            distance = kwargs[_distance]
            #print(currNGram)
            t2Node = tree2.access(currNGram)
            if t2Node is not None:
                distance = distance + metric(si.treeNode, t2Node)
            else:
                distance = distance + metric(si.treeNode, None)

            kwargs[_distance] = distance

        def final(kwargs):
            return kwargs[_distance]

        dicc[_distance] = tree1.searchTree(None, enterN, None, final, **dicc)

        def enterN2(si, currNGram, kwargs):
            distance = kwargs[_distance]
            
            t1Node = tree1.access(currNGram)

            if t1Node is None:
                distance = distance + metric(si.treeNode, None)

            kwargs[_distance] = distance

        return tree2.searchTree(None, enterN2, None, final, **dicc) 
        


    def access(self, postags):
        currNode = self.root
        if postags[0] == "root":
            postags = postags[1:]
        for it in range(0, len(postags)):
            if postags[it] in currNode.children:
                currNode = currNode.children[postags[it]]
            else:
                return None
        return currNode


   


class TreeNode:
    _count = "cn"
    _annotations = "an"
    _children = "ch"
    def __init__(self, annon = None):
        self.count = 0
        if annon is None:
            self.annotations = {}
        else:
            self.annotations = {annon : 0}

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


def wordToPOS(path, rrange = None, rprint = False):
    text = docx2txt.process(path)
    sentences = nltk.sent_tokenize(text)
    words = []
    for x in range(0, len(sentences)):
        tmpsent = nltk.word_tokenize(sentences[x])
        for y in range(0, len(tmpsent)):
            words.append(tmpsent[y])
    tagged = nltk.pos_tag(words)
    POSes = []
    for x in range(0, len(tagged)):
        POSes.append(tagged[x][1])
    if(rrange is None):
        rrange = (0, len(words))
    if(rprint):
        print(words[rrange[0]: rrange[1]])
    return (POSes[rrange[0]:rrange[1]])

def txtToPOS(text):
    sentences = nltk.sent_tokenize(text)
    words = []
    for x in range(0, len(sentences)):
        tmpsent = nltk.word_tokenize(sentences[x])
        for y in range(0, len(tmpsent)):
            words.append(tmpsent[y])
    tagged = nltk.pos_tag(words)
    POSes = []
    for x in range(0, len(tagged)):
        POSes.append(tagged[x][1])
    return POSes

def makeDirIfNec(directoryPath):
    if not os.path.exists(directoryPath):
        os.mkdir(directoryPath)

def writeToNationTree(pathToFile, treeDep, nat, resultDirectoryPath):
    file = open(pathToFile, "r")
    text = file.read()
    file.close()

    natTreeFileName = nat + "_Tree.json"
    newTreeFilePath = os.path.join(resultDirectoryPath, natTreeFileName)

    if not os.path.exists(newTreeFilePath):
        tree = NDictionary(treeDep)
    else:
        tree = NDictionary.fromJSONFile(newTreeFilePath)

    
    tree.addSequence(txtToPOS(text), nat)

    makeDirIfNec(resultDirectoryPath)

    tree.toFile(newTreeFilePath)

def writeToHyperTree(pathToText, treeDepth, nat, directoryName, treePath):
    directoryPath = makeDirIfNec(directoryName)
    if os.path.exists(treePath):
        hyperTree = NDictionary.fromJSONFile(treePath)
    else:
        hyperTree = NDictionary(treeDepth)

    file = open(pathToText, "r")
    text = file.read()
    file.close()

    hyperTree.addSequence(txtToPOS(text), nat)

    hyperTree.toFile(treePath)
