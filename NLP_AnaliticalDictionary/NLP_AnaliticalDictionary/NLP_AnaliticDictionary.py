#from Converter import wordToPOS, txtToPOS, writeToNationTree
from Converter import *
import enum
from NDictionary import *
#from NDictionary import Dicc
import sys
import json
import os
from os import getcwd, path
import ntpath
from pdf2txt import *

def joinTextList(list, sep):
    return sep.join(list)

treeDep = 6           

directoryName = "TReesults"
hyperTreeName = "HyperTree.json"
verbose = False

it = 1
toWrite = []
toWriteNats = []
treesToCmp = []
paths = []

while(it < len(sys.argv)):
    arg = sys.argv[it]
    if arg.startswith("-"):
        curra = arg[1:]
        if curra == "a":
            #dep
            it = it + 1
            toWrite.append(sys.argv[it])
            it = it + 1
            toWriteNats.append(sys.argv[it])

        if curra == "all":
            it = it + 1
            readDirPath = sys.argv[it]
            it = it + 1
            nat = sys.argv[it]

            #for f in os.listdir(readDirPath):
            #    filePath = path.join(readDirPath, f)
            #    if path.isfile(filePath) and filePath.endswith(".txt"):
            #        toWrite.append(filePath)
            #        toWriteNats.append(nat)
            print("loading " + str(nat))
            loaded = load_all(readDirPath, False)
            for load in loaded:
                text = joinTextList(load, " ")
                toWrite.append(text)
                toWriteNats.append(nat)

        if curra == "tall":
            it = it + 1
            path = sys.argv[it]
            files = os.listdir(path)
            for file in files:
                if file.endswith(".pdf"):
                    arg = os.path.join(path, file)
                    conv = convert(arg)[1]
                    conv = joinTextList(conv, " ")
        
                    td = NDictionary(treeDep)
                    td.addSequence(txtToPOS(conv))
                    treesToCmp.append(td)
                    paths.append(arg)

        if curra == "an":
            it = it + 1
            NDictionary.analDepth = sys.argv[it]

        if curra == "v":
            it = it + 1
            arg = sys.argv[it]
            
            if arg == "True":
                verbose = True

        if curra == "d":
            it = it + 1
            directoryName = sys.argv[it]

        if curra == "ht":
            it = it + 1
            hyperTreeName = sys.argv[it]
            if not hyperTreeName.endswith(".json"):
                hyperTreeName = hyperTreeName + ".json"

    else:
        conv = convert(arg)[1]
        #print(conv)
        conv = joinTextList(conv, " ")
        #print(conv)
        
        td = NDictionary(treeDep)
        td.addSequence(txtToPOS(conv))
        treesToCmp.append(td)
        paths.append(arg)
        #print(td.print())
    
    it = it + 1

cwd = getcwd()
            
directoryPath = os.path.join(cwd, directoryName)
hyperTreePath = os.path.join(directoryPath, hyperTreeName) 

if(len(toWrite) > 0):
    makeDirIfNec(directoryPath)
    if os.path.exists(hyperTreePath):
        hyperTree = NDictionary.fromJSONFile(hyperTreePath)
    else:
        hyperTree = NDictionary(treeDep)

    for i in range(0, len(toWrite)):
        text = toWrite[i]
        nat = toWriteNats[i]
        if verbose:
            print("Writing text " + str(i) + " as " + nat)
        #writeToHyperTree(text, treeDep, nat, directoryPath, hyperTreePath)
        hyperTree.addSequence(txtToPOS(text), nat)
        if verbose:
            print("Hyper tree written")
        
    hyperTree.toFile(hyperTreePath)
    if verbose and len(toWrite) > 0:
        print("Writing done")


#ht = NDictionary.fromJSONFile(hyperTreePath)
#print(ht.root.annotations)
#ht = NDictionary.fromJSONFile(hyperTreePath)

if len(treesToCmp) > 0:
    hyperTree = NDictionary.fromJSONFile(hyperTreePath)
    for i in range(0, len(treesToCmp)):
        print(paths[i])
        td = treesToCmp[i]
        #print(NDictionary.analisys(td, hyperTree, verbose))



