import nltk
import docx2txt

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


