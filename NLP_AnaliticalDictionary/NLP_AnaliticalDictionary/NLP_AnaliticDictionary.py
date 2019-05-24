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

treeDep = 6           

directoryName = "TReesults"
hyperTreeName = "HyperTree.json"
verbose = False

it = 1
toWrite = []
toWriteNats = []

while(it < len(sys.argv)):
    arg = sys.argv[it]
    if arg.startswith("-"):
        curra = arg[1:]
        if curra == "a":
            it = it + 1
            toWrite.append(sys.argv[it])
            it = it + 1
            toWriteNats.append(sys.argv[it])

        if curra == "all":
            it = it + 1
            readDirPath = sys.argv[it]
            it = it + 1
            nat = sys.argv[it]

            for f in os.listdir(readDirPath):
                filePath = path.join(readDirPath, f)
                if path.isfile(filePath) and filePath.endswith(".txt"):
                    toWrite.append(filePath)
                    toWriteNats.append(nat)

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
        td = NDictionary.fromTxtFile(arg, treeDep)
    
    it = it + 1

cwd = getcwd()
            
directoryPath = path.join(cwd, directoryName)
hyperTreePath = path.join(directoryPath, hyperTreeName) 

for i in range(0, len(toWrite)):
    path = toWrite[i]
    nat = toWriteNats[i]
    if verbose:
        print("Writing " + path + " as " + nat)
    writeToHyperTree(path, treeDep, nat, directoryPath, hyperTreePath)
    if verbose:
        print("Hyper tree written")
if verbose and len(toWrite) > 0:
    print("Writing done")

ht = NDictionary.fromJSONFile(hyperTreePath)

print(NDictionary.analisys(td, ht))
