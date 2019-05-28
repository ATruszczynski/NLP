from StackItem import *
import nltk
import docx2txt
#from NDictionary import *
import sys
import json
import os
import ntpath
from math import sqrt
from pdf2txt import *
import pdf2txt
import copy

class NDictionary(object):
    toRemove = list(("\"", ":", ";", "(", ")", " ", "",'', "...",'','``',"''", "\n"))
    _maxDepth = "mdk"
    _root = "rk"
    distance = "distance"
    signN = "sign"
    maxi = 20
    minAnalDepth = 6
    maxAnalDepth = 6

    htt = 1
    eucc = 1.5
    chartol = 1.1
    dealbreaker = [5, 3, 4, 2, 1, 0]

    _sim = "sim"
    _euc2 = "euc2"
    _euc3 = "euc3"
    _cos = "cos"
    _char = "char"

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

    def fromTagFile(path, treeDep):
       result = NDictionary(treeDep)
       tags = tagsFromTagFile(path)
       result.addSequence(tags)
       return result



    def fromTxtFile(path, treeDep):
        file = open(path, "r", encoding="utf-8")
        text = file.read()
        file.close()

        tree = NDictionary(treeDep)
        tree.addSequence(txtToPOS(text))
        return tree

    def add(self, ngram, annotation):
        currentNode = self.root
        for i in range(0, len(ngram)):
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
        sequence = filterr(sequence, self.toRemove)
        toAdd = []
        for i in range(0, len(sequence)):
            toAdd.append(sequence[i])
            if(len(toAdd) == self.maxDepth):
                self.add(toAdd, annotation)
                toAdd = toAdd[1:]
        while len(toAdd) > 0:
            self.add(toAdd, annotation)
            toAdd = toAdd[1:]




        
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
                if si.depth < NDictionary.maxAnalDepth:
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

    def mostPopular2(self, minDepth, maxDepth, nat, howMany = -1):
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

    def HTTicks(tree, hyperTree, pow = 1):
        _currTick = "currTicks"
        _signN = NDictionary.signN
        dicc = {}
        for nat in hyperTree.root.annotations:
            dicc[nat] = ResultTuple(nat, NDictionary._sim, [])
        def enterN(si, currNGram, kwargs):
            
            
            if(si.depth >= NDictionary.minAnalDepth):
                htnode = hyperTree.access(currNGram)
                if htnode is not None:
                    for nat in htnode.annotations:
                        toAdd = (htnode.annotations[nat]/hyperTree.root.annotations[nat]) ** pow

                        kwargs[nat].reasoning = addToSortedListOfNGTup(kwargs[nat].reasoning, NGramTuple(currNGram.copy(), toAdd), True)
                        kwargs[nat].score = kwargs[nat].score + toAdd

            
        
        def final(kwargs):
            
            dicc = sortDictByValue(kwargs, True, lambda x : kwargs[x].score)
            
            return dicc[getDictKey(dicc, 0)]
        return tree.searchTree(None, enterN, None, final, **dicc)

    def characteristic(tree, ht, tol = 2):
        _currTick = "currTicks"
        dicc = {}
        for nat in ht.root.annotations:
            dicc[nat] = ResultTuple(nat, NDictionary._char, [])
        def enterN(si, currNGram, kwargs):
            if(si.depth >= NDictionary.minAnalDepth):
                htnode = ht.access(currNGram)
                if htnode is not None:
                    ht_an = htnode.annotations.copy()
                    for it in ht_an:
                        ht_an[it] = ht_an[it]/ht.root.annotations[it]
                    sort_ann = sortDictByValue(ht_an, True)

                    sav = list(sort_ann.values())
                    if (len(sav) > 1 and sav[0] > tol * sav[1]) or len(sav) == 1:
                        ann = getDictKey(sort_ann, 0)

                        if len(sav) == 1:
                            toAdd = 5*tol
                        else:
                            toAdd = sav[0]/sav[1]

                        kwargs[ann].reasoning = addToSortedListOfNGTup(kwargs[ann].reasoning, NGramTuple(currNGram.copy(), toAdd), True)
                        kwargs[ann].score = kwargs[ann].score + toAdd
                        


            #kwargs[_currTick] = currTick

        def final(kwargs):

            return kwargs

        dicc = tree.searchTree(None, enterN, None, final, **dicc)
        dicc = sortDictByValue(dicc, True, lambda x : dicc[x].score)

        return dicc[getDictKey(dicc, 0)]

    def countNats(self):
        _counts = "counts"
        dicc = {_counts: {} }
        def enterN(si, currNGram, kwargs):
            counts = kwargs[_counts]
            
            if si.depth >= NDictionary.minAnalDepth:
                for nat in si.treeNode.annotations:
                    if nat not in counts:
                        counts[nat] = 0
                    counts[nat] = counts[nat] + 1
            

            kwargs[_counts] = counts
        def final(kwargs):
            return kwargs[_counts]
        return self.searchTree(None, enterN, None, final, **dicc)
    
    def simpleMetricComp(tree, ht, metric, reversed = False):
        _distance = NDictionary.distance
        _signN = NDictionary.signN
        dicc = {}
        for natt in ht.root.annotations:
            dicc[natt] = { _distance : 0, _signN: [] }

        def enterN(si, currNGram, kwargs):
            for nat in ht.root.annotations:
                curr = kwargs[nat]
                distance = curr[_distance]
                signN = curr[_signN]

                if(si.depth >= NDictionary.minAnalDepth):
                    htNode = ht.access(currNGram, nat)
                    if htNode is not None:
                        #distance = distance + metric(si.treeNode.count/tree.root.count, htNode.annotations[nat]/ht.root.annotations[nat])
                        toAdd = metric(si.treeNode.count/tree.root.count, htNode.annotations[nat]/ht.root.annotations[nat])
                    else:
                        #distance = distance + metric(si.treeNode.count/tree.root.count, 0)
                        toAdd = metric(si.treeNode.count/tree.root.count, 0)

                    tal = NGramTuple(currNGram.copy(), toAdd)
                    signN = addToSortedListOfNGTup(signN, tal, reversed)

                    distance = distance + toAdd

                curr[_distance] = distance
                curr[_signN] = signN
                kwargs[nat] = curr

        def final(kwargs):
            return kwargs

        dicc = tree.searchTree(None, enterN, None, final, **dicc)

        #print(dicc)

        def enterN2(si, currNGram, kwargs):
            for nat in ht.root.annotations:
                curr = kwargs[nat]
                distance = curr[_distance]

                if(si.depth >= NDictionary.minAnalDepth):
                    if nat in si.treeNode.annotations:
                        treeNode = tree.access(currNGram)
                        if treeNode is None:
                            distance = distance + metric(si.treeNode.annotations[nat]/ht.root.annotations[nat], 0)

                curr[_distance] = distance
                kwargs[nat] = curr

        dicc = ht.searchTree(None, enterN2, None, final, **dicc) 
        #print(dicc)

        dicc = sortDictByValue(dicc, reversed, lambda x : dicc[x][_distance])
        nat = getDictKey(dicc, 0)
        result = dicc[nat]

        resultT = ResultTuple(nat, "", result[_signN])
        resultT.score = result[_distance]

        return resultT

    def cosineWithHt(tree, ht):
        _AA = "A"
        _BB = "B"
        _AB = "AB"
        _signN = NDictionary.signN
        _distance = NDictionary.distance
        dicc = {}
        for nat in ht.root.annotations:
            dicc[nat] = { _AB : 0, _AA : 0, _BB : 0, _signN: [] }
        def enterN1(si, currNGram, kwargs):
            for nat in ht.root.annotations:
                curr = kwargs[nat]
                AB = curr[_AB]
                AA = curr[_AA]
                signN = curr[_signN]

                if(si.depth >= NDictionary.minAnalDepth):
                    htNode = ht.access(currNGram, nat)
                    if htNode is not None:
                        toAdd = (si.treeNode.count/tree.root.count)*(htNode.annotations[nat]/ht.root.annotations[nat])
                        AB = AB + toAdd
                        signN = addToSortedListOfNGTup(signN, NGramTuple(currNGram.copy(), toAdd), True)

                    AA = AA + (si.treeNode.count/tree.root.count)**2

                curr[_AB] = AB
                curr[_AA] = AA
                curr[_signN] = signN
                kwargs[nat] = curr

        def final1 (kwargs):
            return kwargs#{ _AA : kwargs[_AA], _AB : kwargs[_AB], _signN : kwargs[_signN] }

        dicc = tree.searchTree(None, enterN1, None, final1, **dicc)
        #dicc[_AA] = tDicc[_AA]
        #dicc[_AB] = tDicc[_AB]
        #dicc[_signN] = tDicc[_signN]

        def enterN2(si, currNGram, kwargs):
            for nat in ht.root.annotations:
                curr = kwargs[nat]
                BB = curr[_BB]

                if(si.depth >= NDictionary.minAnalDepth):
                    if nat in si.treeNode.annotations:
                        BB = BB + (si.treeNode.annotations[nat]/ht.root.annotations[nat])**2
            
                curr[_BB] = BB
                kwargs[nat] = curr

        def final2(kwargs):
            return { _BB : kwargs[_BB] }

        dicc = ht.searchTree(None, enterN2, None, final1, **dicc)
        #dicc[_BB] = tDicc[_BB]

        result = {}
        for nat in ht.root.annotations:
            curr = dicc[nat]
            curr = { NDictionary.distance: curr[_AB]/(sqrt(curr[_AA])*sqrt(curr[_BB])), NDictionary.signN : curr[NDictionary.signN] }
            result[nat] = curr
            
        dicc = sortDictByValue(result, True, lambda x : result[x][_distance])
        nat = getDictKey(dicc, 0)
        result = dicc[nat]
        

        resultT = ResultTuple(nat, NDictionary._cos , result[_signN])
        resultT.score = result[_distance]

        return resultT
        
    def analisys(tree, ht, verbose = False):
        dicc1 = NDictionary.HTTicks(tree, ht, NDictionary.htt)

        def euc3Metric(n1, n2):
            return (abs(n1 - n2))**NDictionary.eucc
        
        euc3 = NDictionary.simpleMetricComp(tree, ht, euc3Metric)
        euc3.source = NDictionary._euc3

        def euc2Metric(n1, n2):
            return (n1 - n2)**2

        euc2 = NDictionary.simpleMetricComp(tree, ht, euc2Metric)
        euc2.source = NDictionary._euc2

        cos = NDictionary.cosineWithHt(tree, ht)
        
        dicc2 = NDictionary.characteristic(tree, ht, NDictionary.chartol)

        if verbose:
            print("Sim")
            print(dicc1)
            print("Euc")
            print(euc3)
            print("Euc2")
            print(euc2)
            print("cos")
            print(cos)
            print("char")
            print(dicc2)

        return [dicc1, euc2, euc3, cos, dicc2, dicc2]

    def access(self, postags, nation = None):
        currNode = self.root
        if postags[0] == "root":
            postags = postags[1:]
        for it in range(0, len(postags)):
            if postags[it] in currNode.children:
                currNode = currNode.children[postags[it]]
            else:
                return None
        if nation is None:
            return currNode
        if nation in currNode.annotations:
            return currNode
        else:
            return None

    def touch(self, postags, count, annotations):
        currNode = self.root
        it = 1
        while it < len(postags):
            if postags[it] in currNode.children:
                currNode = currNode.children[postags[it]]
            else:
                currNode.children[postags[it]] = TreeNode()
                currNode = currNode.children[postags[it]]
            it = it + 1
        currNode.count = count
        currNode.annotations = annotations
        


   


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



def filterr(sequence, toRemove):
    sequence = list(sequence)
    last = None
    nnps = list(("NNP", "NNPS", "NN", "JJ"))
    result = []

    for nn in nnps:
        tmp = []
        for it in range(0, len(sequence)):
            if(sequence[it] == nn and last == nn):
                continue
            if(not (sequence[it] in toRemove)):
                tmp.append(sequence[it])
            last = sequence[it]
        sequence = tmp

    toKeep = []
    for i in range(0, len(sequence)):
        toKeep.append(True)
    for it in range(2, len(sequence)):
        if sequence[it - 2 : it + 1] in [["JJ", "NN", "JJ"], ["NN", "JJ", "NN"], ["NN", "NNP", "NN"], ["NNP", "NN", "NNP"]]:
            toKeep[it - 2 : it + 1] = [False]*3
            continue

    tmp = []
    for i in range(0, len(sequence)):
        if toKeep[i]:
            tmp.append(sequence[i])

    sequence = tmp

    result = sequence
    return result

def listEq(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(0, len(l1)):
        if l1[i] != l2[i]:
            return False
    return True

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

#def writeToHyperTree(pathToText, treeDepth, nat, directoryName, treePath):
#    directoryPath = makeDirIfNec(directoryName)
#    if os.path.exists(treePath):
#        hyperTree = NDictionary.fromJSONFile(treePath)
#    else:
#        hyperTree = NDictionary(treeDepth)

#    file = open(pathToText, "r", encoding="utf-8")
#    text = file.read()
#    file.close()

#    #print(text)

#    hyperTree.addSequence(txtToPOS(text), nat)

#    hyperTree.toFile(treePath)


def writeToHyperTree(text, treeDepth, nat, directoryName, treePath):
    directoryPath = makeDirIfNec(directoryName)
    if os.path.exists(treePath):
        hyperTree = NDictionary.fromJSONFile(treePath)
    else:
        hyperTree = NDictionary(treeDepth)

    #file = open(pathToText, "r", encoding="utf-8")
    #text = file.read()
    #file.close()

    #print(text)

    hyperTree.addSequence(txtToPOS(text), nat)

    hyperTree.toFile(treePath)


def sortDictByValue(dict,  reversed = False, _key = None):
    if _key is None:
        _key = dict.get
    ct_sort_keys = sorted(dict, key=_key, reverse=reversed)
    result = {}
    for r in ct_sort_keys:
        result[r] = dict[r]
    return result

def getDictKey(dict, ind):
    if(len(dict) == 0):
        return None
    return list(dict.keys())[ind]

def tagsFromTagFile(path):
    readSent = load(path)
    readPairs = []
    for sent in readSent:
        readPairs.extend([pair for pair in sent])
    return [pair[1] for pair in readPairs]

def addToSortedListOfNGTup(list, elem, reveersed = False):
    list.append(elem)
    list = sorted(list, key = lambda x: x.value, reverse = reveersed)
    if(len(list) > NDictionary.maxi):
        list.pop()
    return list

def printLNG(l):
    for i in l:
        print(str(i.ngram) + " - " + str(i.value))

def analisysResult(anal):
    
    anal[0].dealbreaker, anal[1].dealbreaker, anal[2].dealbreaker, anal[3].dealbreaker,  anal[4].dealbreaker, anal[5].dealbreaker = NDictionary.dealbreaker

    prop = {}

    for a in anal:
        propa = a.answer
        if propa not in prop:
            prop[propa] = 0
        prop[propa] = prop[propa] + 1
    
    prop = sortDictByValue(prop, True)

    max = prop[getDictKey(prop, 0)]

    possible_ans = []
    for ans in prop:
        if prop[ans] == max:
            possible_ans.append(ans)
    
    

    resultTups = []
    for an in anal:
        if an.answer in possible_ans:
            resultTups.append(an)
    
    
    
    resultTups = sorted(resultTups, key = lambda x : x.dealbreaker, reverse = True)

    
    return resultTups[0]

def getNationality(path, ht_path):
    if path.endswith(".pdf"):
        conv = pdf2txt._convert(path)[0]
    elif path.endswith("_output.txt"):
        conv = pdf2txt.load(path, False)

    text = " ".join(conv)

    td = NDictionary(NDictionary.maxAnalDepth)
    for sentence in conv:
        td.addSequence(txtToPOS(sentence))

    print(td.print())

    hyperTree = NDictionary.fromJSONFile(ht_path)

    anal = NDictionary.analisys(td, hyperTree)
    pre_result = analisysResult(anal)

    _sign = "Sign"
    result = { "Nat": pre_result.answer, _sign : [] }

    
    print(pre_result.source)

    for ngramT in pre_result.reasoning:
        for sentence in conv:
            ngram = ngramT.ngram[1:]
            #print("sear: " + str(ngram))
            result[_sign].extend(findWordsFromTags(sentence, ngram))

    return result

def findWordsFromTags(text, tags):
    sentences = nltk.sent_tokenize(text)
    words = []
    for x in range(0, len(sentences)):
        tmpsent = nltk.word_tokenize(sentences[x])
        for y in range(0, len(tmpsent)):
            words.append(tmpsent[y])
    tagged = nltk.pos_tag(words)

    result = []
    #print("search")
    for i in range(0, len(tagged) - len(tags)):
        #print(tagged[i][1] + " ?= " + tags[0])
        if tagged[i][1] == tags[0]:
            ok = True
            for tagit in range(0, len(tags)):
                #print(str(2) + " " + tagged[i + tagit][1] + " ?= " + tags[tagit])
                if tagged[i + tagit][1] != tags[tagit]:
                    ok = False 
            if ok:
                #print("ok")
                toAdd = []
                for tit in range(0, len(tags)):
                    toAdd.append(tagged[i + tit][0])
                result.append(toAdd)
    return result




