from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
import os
import sys
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re

from functools import reduce


addon_to_name = '_output'
minimal_ratio_of_letters_to_text = 0.5
minimal_length = 7
paragraphs = list()
out_paragraphs = list()

def use_sentence(sentence, l):
    tokenizer = RegexpTokenizer(r'\w+')
    words = [w for w in tokenizer.tokenize(sentence) if w not in stopwords.words('english')]
    if len(words) < l:
        return None
    tags = nltk.pos_tag(words)
    (n, v, o) = count_tags(tags)
    return tags if (o != 0 and n < 0.9 and v > 0.01) else None

def count_tags(tags):
    counters = list((0, 0, 0))
    num = len(tags)
    if num == 0:
        return counters
    for (word, tag) in tags:
        if tag[0] == 'N':
            counters[0] += 1
        elif tag[0] == 'V':
            counters[1] += 1
        else:
            counters[2] += 1
    return (counters[0]/num, counters[1]/num, counters[2]/num)

def use_paragraph(paragraph):
    if paragraph in paragraphs:
        if paragraph in out_paragraphs:
            out_paragraphs.remove(paragraph)
        return

    if not use_sentence(paragraph, 10):
        return
    
    paragraphs.append(paragraph)
    num_letters = reduce(lambda num, char: num + (1 if char.isalpha() else 0), paragraph, 0)
    len_text = len(paragraph)
    if len_text >= minimal_length and num_letters / len_text > minimal_ratio_of_letters_to_text:
        out_paragraphs.append(paragraph)


def process(paragraph):

    paragraph = paragraph.replace('-\n', '')
    paragraph = paragraph.replace('\n', ' ')
    paragraph = paragraph.replace('\ufb00', 'ff')
    paragraph = paragraph.replace('\ufb01', 'fi')
    paragraph = paragraph.replace('\ufb02', 'fl')
    paragraph = paragraph.replace('\ufb03', 'ffi')
    paragraph = paragraph.replace('\ufb04', 'ffl')
    paragraph = paragraph.replace('Fig.', ' ')
    paragraph = re.sub(r'\[[\d, ]+\]', ' ', paragraph)
    return paragraph

def filter_sentences(sentences, tags):
    out_sentences = list()
    for sentence in sentences:
        tagged = use_sentence(sentence, 2)
        if tagged and sentence[0].isupper():
            out_sentences.append(tagged if tags else sentence)
    return out_sentences

# converts pdf, returns list of sentences
def convert(filename, tags=False):
    pagenums = set()
    laparams = LAParams(line_margin=0.15)
    output = StringIO()
    manager = PDFResourceManager()
    device = PDFPageAggregator(manager, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, device)

    with open(filename, 'rb') as infile:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal) or isinstance(element, LTTextLineHorizontal):
                    paragraph = element.get_text()
                    use_paragraph(paragraph)

    text = reduce(lambda text, paragraph : text + process(paragraph), out_paragraphs, '')
    sentences = filter_sentences(nltk.sent_tokenize(text), tags)
    if len(sentences) < 20:
            #Something went wrong during text parsing
            sys.stderr.write('Error occured in sentence parsing file: ' + filename + '\n')
            return None
    return sentences

def loadall(path):
    files = list()
    for item in os.listdir(path):
        extension = item.split('.')[-1].lower()
        if extension == 'txt':
            files.append(item)
    documents = list()
    for file in files:
        doc = list()
        with open(file, 'r') as f:
            doc = f.readlines()
            tokenizer = RegexpTokenizer(r'\w+')
            words_list = [tokenizer.tokenize(sentence) for sentence in doc]
            tags = [nltk.pos_tag(words) for words in words_list]
            documents.append(tags)

def load(file):
    with open(file, 'r', encoding='utf-8') as f:
        doc = f.readlines()
        tokenizer = RegexpTokenizer(r'\w+')
        words_list = [tokenizer.tokenize(sentence) for sentence in doc]
        tags = [nltk.pos_tag(words) for words in words_list]
    return tags

def loadall(path):
    files = list()
    for item in os.listdir(path):
        extension = item.split('.')[-1].lower()
        if extension == 'txt':
            files.append(item)
    documents = list()
    print(files)
    for file in files:
        file = os.path.join(path, file)
        print(file)
        documents.append(load(file))
    return documents


if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    files_to_convert = []
    for item in os.listdir():
        extension = item.split('.')[-1].lower()
        if extension == 'pdf':
            files_to_convert.append(item)

    for file in files_to_convert:
        output_name = file.split('.')[0] + addon_to_name + ".txt"
        print('Converting ' + file)
        with open(output_name, 'wt', encoding='utf-8') as f:
            try:
                sentences = convert(file)
            except PDFTextExtractionNotAllowed:
                sys.stderr.write('Could not extract text from file: ' + file + '\n')
            if sentences:
                for s in sentences:
                    f.write(s + '\n')






