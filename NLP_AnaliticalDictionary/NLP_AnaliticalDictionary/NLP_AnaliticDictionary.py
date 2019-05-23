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

pathh = "C:\\Users\\Aleksander\\Downloads\\KorraAV.docx"
#pathh = "C:\\Users\\Aleksander\\Downloads\\BackToUs.docx"

pathhh = "C:\\Users\\Aleksander\\Desktop\\NLP_test_folder\\Nowyfolder\\Fairgame.txt"
pathhhh = "C:\\Users\Aleksander\\source\\repos\\NLP_Final\\NLP\\NLP_AnaliticalDictionary\\NLP_AnaliticalDictionary\\Test.txt"



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
            it = it + 1

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
            
            it = it + 1

        if curra == "v":
            it = it + 1
            arg = sys.argv[it]
            
            if arg == "True":
                verbose = True

            it = it + 1

        if curra == "d":
            it = it + 1
            directoryName = sys.argv[it]
            it = it + 1
        if curra == "ht":
            it = it + 1
            hyperTreeName = sys.argv[it]
            if not hyperTreeName.endswith(".json"):
                hyperTreeName = hyperTreeName + ".json"
            it = it + 1
            
             




        




cwd = getcwd()
            
directoryPath = path.join(cwd, directoryName)
hyperTreePath = path.join(directoryPath, hyperTreeName) 

for i in range(0, len(toWrite)):
    path = toWrite[i]
    nat = toWriteNats[i]
    if verbose: 
        print(ntpath.basename(path) + " - " + nat)
    writeToNationTree(path, treeDep, nat, directoryPath)
    if verbose:
        print("Nat tree written")
    writeToHyperTree(path, treeDep, nat, directoryPath, hyperTreePath)
    if verbose:
        print("Hyper tree written")
if verbose and len(toWrite) > 0:
    print("Writing done")






ht = NDictionary.fromJSONFile(hyperTreePath)

#print(ht.mostPopular(3,5, 10))

td = NDictionary.fromTxtFile(pathhhh, treeDep)

dicc = NDictionary.HTTicks(td, ht)

print(dicc)






#treeDep = 5
#minLen = 2
#maxLen = 2
#firstN = 25

#td = NDictionary(maxLen)

##print(txtToPOS(pathhh))

##td.addSequence(wordToPOS(pathh), "PL")

#td.addSequence(txtToPOS(pathhh), "EN")

#print(td.print())
#print(td.mostPopular(minLen,maxLen,firstN))

#print(NDictionary.fromDict(json.loads(json.dumps(td.toJSON()))).mostPopular(minLen, maxLen, firstN))




#if(len(sys.argv) > 1):
#    pathh = sys.argv[1]
#if(len(sys.argv) == 5):
#    treeDep = sys.argv[2]
#    minLen = sys.argv[3]
#    maxLen = sys.argv[4]
#    firstN = sys.argv[5]



##td.addSequence(wordToPOS(pathh), "EN")

##d = NDictionary.fromString("d")



#print(pathh)
##print(td.root.count)

##print(json.dumps(td))





#desu = "Desu.txt"

##td.toFile(desu)

##td2 = NDictionary.fromFile(desu)

##print(td2.mostPopular(minLen, maxLen, firstN))

#cwd = os.getcwd()
#print(cwd)

#resPath = os.path.join(cwd, resultPath)

#if not os.path.exists(resPath):
#    os.mkdir(resPath)

#filePath = os.path.join(resPath, desu)

#td.toFile(filePath)

#print(ntpath.basename(filePath))

