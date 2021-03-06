import enum
from NDictionary import *
#from NDictionary import Dicc
import sys
import json
import os
from os import getcwd, path
import ntpath
from pdf2txt import *
import pdf2txt
import networkx as nx
import matplotlib.pyplot as plt

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
answers = []

tests = []
_answer = "ans"
_trees = "tree"
_paths = "paths"

pdf = False

ans = "EN"

while(it < len(sys.argv)):
    arg = sys.argv[it]
    if arg.startswith("-"):
        curra = arg[1:]
        if curra == "ans":
            it = it + 1
            ans = sys.argv[it]

        if curra == "a":
            it = it + 1
            readFilePath = sys.argv[it]
            it = it + 1
            nat = sys.argv[it]
            loaded = load(readFilePath, False)
            for sentence in loaded:
                toWrite.append(sentence)
                toWriteNats.append(nat)


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
            loaded = load_all(readDirPath, False, True)
            for text in loaded:
                for sentence in text:
                    toWrite.append(sentence)
                    toWriteNats.append(nat)

        if curra == "tall":
            it = it + 1
            path = sys.argv[it]
            it = it + 1
            answ = sys.argv[it]

            test = {_answer : answ, _trees : [], _paths : [] }
            print("Reading: " + path)
            files = os.listdir(path)
            for file in files:
                arg = os.path.join(path, file)
                if file.endswith(".txt") or file.endswith(".pdf"):
                    
                    #print(td.print())
                    #test[_trees].append(td)
                    test[_paths].append(arg)
            #print(test)
            tests.append(test)
            
            print("Test completed " + answ)

        if curra == "p":
            it = it + 1
            pdf = sys.argv[it]
            
        if curra == "man":
            it = it + 1
            
            NDictionary.minAnalDepth = int(sys.argv[it])    

        if curra == "Man":
            it = it + 1
            
            NDictionary.maxAnalDepth = int(sys.argv[it])

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
        print(arg)
        #conv = pdf2txt._convert(arg)[1]
        #td = NDictionary(treeDep)
        
        #for sentence in conv:
        #    td.addSequence(txtToPOS(sentence))

        #treesToCmp.append(td)
        paths.append(arg)
    
    it = it + 1

cwd = getcwd()
            
directoryPath = os.path.join(cwd, directoryName)
hyperTreePath = os.path.join(directoryPath, hyperTreeName) 

if verbose:
    print("1")

#tworzenie Hyper Tree
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
        
    hyperTree.toFile(hyperTreePath)
    if verbose and len(toWrite) > 0:
        print("Writing done")


if verbose:
    print("2")
#ht = NDictionary.fromJSONFile(hyperTreePath)
#print(ht.root.annotations)
#ht = NDictionary.fromJSONFile(hyperTreePath)

if len(paths) > 0:
    hyperTree = NDictionary.fromJSONFile(hyperTreePath)
    for i in range(0, len(paths)):
        result = getNationality(paths[i], hyperTreePath)

        print(result)

_count = "count"
_totCor = "totCor"
results2 = []
results = {_count : 0 }
tot = 0


if verbose:
    print("3")

#if len(treesToCmp) > 0:
#    hyperTree = NDictionary.fromJSONFile(hyperTreePath)
#    for i in range(0, len(treesToCmp)):
#        print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#        print(paths[i])
#        td = treesToCmp[i]
#        anal = NDictionary.analisys(td, hyperTree, verbose)
#        tmpTot = 0
#        for an in anal:
#            if anal[an] == ans:
#                if an not in results:
#                    results[an] = 0
#                results[an] = results[an] + 1
#                tmpTot = tmpTot + 1
#        if tmpTot >= 2: ########################################################## Tu nie 2 raczej
#            tot = tot + 1
#        results[_count] = results[_count] + 1
#        print(anal)
#        print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")


if verbose:
    print("4")

if len(tests) > 0:
    print("start ht load")
    hyperTree = NDictionary.fromJSONFile(hyperTreePath)
    print("HT loaded")
    tresh = 3 if len(hyperTree.root.annotations) == 2 else 2
    for test in tests:
        ans = test[_answer]
        result = {_answer : ans, _count : 0, _totCor : 0 }
        for i in range(0, len(test[_paths])):
            tpath = test[_paths][i]
            print(tpath)
        
            if tpath.endswith(".pdf") and pdf:
                conv = pdf2txt._convert(tpath)[0]
            elif tpath.endswith(".txt") and not pdf:
                conv = load(tpath, False)
                    
        
            td = NDictionary(treeDep)
            for sentence in conv:
                td.addSequence(txtToPOS(sentence))

            #td = test[_trees][i]
            anal = NDictionary.analisys(td, hyperTree, verbose)
            corr = 0
            del td

            for an in anal:
                source = an.source
                if source not in result:
                    result[source] = 0
                if an.answer == ans:
                    result[source] = result[source] + 1
                #anal_answer = an.answer
                #if anal_answer not in result:
                #    result[anal_answer] = 0
                #if anal_answer == ans:
                #    result[anal_answer] = result[anal_answer] + 1
                #    #corr = corr + 1
            
            propAnswer = analisysResult(anal)
            
            if propAnswer.answer == ans:
                result[_totCor] = result[_totCor] + 1
            
            print(propAnswer.answer)
            #if corr >= tresh:
            #    result[_totCor] = result[_totCor] + 1
            result[_count] = result[_count] + 1
            #print(anal)
            print("///////////////////////////////////////////////////////")
        results2.append(result)

for result in results2:
    
    result[NDictionary._char] = result[NDictionary._char]/2
    print(result)
    div = result[_count]
    if div != 0:
        for an in result:
            if an != _answer:
                result[an] = result[an]/div
        print(result)
        print(result[_answer] + " - " + str(result[_totCor] * 100) + " %")
        print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////") 

#if(results[_count] != 0):
#    print(results)
#    div = results[_count]
#    for an in results:
#        results[an] = results[an]/div
#    print(results)
#    print(tot/div)


#hyperTree = NDictionary.fromJSONFile(hyperTreePath)
#print(hyperTree.countNats())
#print(hyperTree.mostPopular(6,6))

#text = "Twitter outrage over image search results of black and white teens is misdirected"

#tag = txtToPOS(text)

#print(findWordsFromTags(text, ["CC", "JJ"]))





