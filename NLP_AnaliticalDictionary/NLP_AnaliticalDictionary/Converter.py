import nltk
import docx2txt
from NDictionary import *
import sys
import json
import os
import ntpath

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
        tree = NDictionary.fromFile(newTreeFilePath)

    
    tree.addSequence(txtToPOS(text), nat)

    makeDirIfNec(resultDirectoryPath)

    tree.toFile(newTreeFilePath)

def writeToHyperTree(pathToText, treeDepth, nat, directoryName, treePath):
    directoryPath = makeDirIfNec(directoryName)
    if os.path.exists(treePath):
        hyperTree = NDictionary.fromFile(treePath)
    else:
        hyperTree = NDictionary(treeDepth)

    file = open(pathToText, "r")
    text = file.read()
    file.close()

    hyperTree.addSequence(txtToPOS(text), nat)

    hyperTree.toFile(treePath)



