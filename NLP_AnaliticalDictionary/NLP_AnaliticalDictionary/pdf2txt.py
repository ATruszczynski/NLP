import os
import os.path
import sys

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
from tika import parser


addon_to_name = '_output'
addon_to_name_short = '_output_short'
sw = stopwords.words('english')


def _tokenize(sentence):
    tokenizer = RegexpTokenizer(r'[a-zA-Z][a-zA-Z]+')
    words = tokenizer.tokenize(sentence)
    return words


def _use_sentence(sentence, l):
    words = _tokenize(sentence)
    words_without_stop = [w for w in words if w not in sw]
    if len(words) < l:
        return None, None
    tags = nltk.pos_tag(words)
    (n, v, o) = _count_tags(tags)
    use = o != 0 and n < 0.99 and v != 0
    if use:
        return ' '.join(words), ' '.join(words_without_stop)
    return None, None


def _count_tags(tags):
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
    return counters[0] / num, counters[1] / num, counters[2] / num


def _process(paragraph):
    paragraph = re.sub(r'-$', '', paragraph)
    paragraph = paragraph.replace('\ufb00', 'ff')
    paragraph = paragraph.replace('\ufb01', 'fi')
    paragraph = paragraph.replace('\ufb02', 'fl')
    paragraph = paragraph.replace('\ufb03', 'ffi')
    paragraph = paragraph.replace('\ufb04', 'ffl')
    paragraph = paragraph.replace('Fig.', ' ')
    paragraph = paragraph.replace('e.g.', ' ')
    paragraph = re.sub(r'\[[\d, ]+\]', ' ', paragraph)
    return paragraph


def _filter_sentences(sentences):
    sentences_all = list()
    sentences_short = list()
    for sentence in sentences:
        s1, s2 = _use_sentence(sentence, 2)
        if s1:
            sentences_all.append(s1)
            sentences_short.append(s2)
    return sentences_all, sentences_short


# Does nothing now
def _remove_beginning(lines):
    return lines


def _connect_lines_into_sentences(lines):
    lines = _remove_beginning(lines)
    lines = [_process(line) for line in lines]
    text = ''.join(map(str, lines))
    return text


def convert(filename):
    pdf_parser = parser.from_file(filename)
    if not 'content' in pdf_parser:
        sys.stderr.write('Could not open file ' + filename + '\n')
        return None, None
    pdf_text = pdf_parser['content']
    content = []
    for item in pdf_text.splitlines():
        if item is not '':
            if re.match(r'^\w+', item):
                content.append(item)
    sentences = _connect_lines_into_sentences(content)
    return _filter_sentences(nltk.sent_tokenize(sentences))


def load(file_name, tags=True):
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.readlines()
        if not tags:
            return content
        sentences_words = [_tokenize(line) for line in content]
        tags = [nltk.pos_tag(words) for words in sentences_words]
        return tags


def load_all(path='.', tags=True, include_stopwords=False):
    all_files = os.listdir(path)
    addon = addon_to_name if include_stopwords else addon_to_name_short
    files = [f for f in all_files if re.match('.*' + addon + '.txt', f)]
    for f in files:
        yield load(os.path.join(path, f), tags)


if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    files_to_convert = []
    for item in os.listdir('.'):
        extension = item.split('.')[-1].lower()
        if extension == 'pdf':
            files_to_convert.append(item)

    for file in files_to_convert:
        print('Converting ' + file)
        output_name = file.split('.')[0] + addon_to_name + ".txt"
        output_name_short = file.split('.')[0] + addon_to_name_short + ".txt"
        out_sentences, out_short_sentences = convert(file)
        if out_sentences:
            with open(output_name, 'wt', encoding='utf-8') as f, open(output_name_short, 'wt', encoding='utf-8') as f2:
                for s in out_sentences:
                    f.write(s + '\n')
                for s in out_short_sentences:
                    f2.write(s + '\n')
    print('done!')
