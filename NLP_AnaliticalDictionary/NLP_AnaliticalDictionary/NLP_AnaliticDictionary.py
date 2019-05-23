from Converter import wordToPOS
import enum
from NDictionary import NDictionary
#from NDictionary import Dicc
import sys
import json
import os

pathh = "C:\\Users\\Aleksander\\Downloads\\KorraAV.docx"
#pathh = "C:\\Users\\Aleksander\\Downloads\\BackToUs.docx"

resultPath = "TReesults"

treeDep = 5
minLen = 2
maxLen = 2
firstN = 25
if(len(sys.argv) > 1):
    pathh = sys.argv[1]
if(len(sys.argv) == 5):
    treeDep = sys.argv[2]
    minLen = sys.argv[3]
    maxLen = sys.argv[4]
    firstN = sys.argv[5]


td = NDictionary(maxLen)
td.addSequence(wordToPOS(pathh), "PL")

#td.addSequence(wordToPOS(pathh), "EN")

#d = NDictionary.fromString("d")



print(pathh)
#print(td.root.count)

#print(json.dumps(td))



#print(td.print())
print(td.mostPopular(minLen,maxLen,firstN))

desu = "Desu.txt"

#td.toFile(desu)

#td2 = NDictionary.fromFile(desu)

#print(td2.mostPopular(minLen, maxLen, firstN))

cwd = os.getcwd()
print(cwd)

resPath = os.path.join(cwd, resultPath)

os.mkdir(resPath)

