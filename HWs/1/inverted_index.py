#################################################################################################
# This script creates an inverted index for a given input file (containing multiple documents).
# Procedures:
#   1. Parse document (according to its specific syntax) and create docID-doc dictionary
#   2. Apply text normalization and store in docID-(tokenSet) format
#   3. Construct inverted index and store the output (in text file and dictionary)
# To run:
#   python inverted_index.py
#################################################################################################

import re
import nltk
import pickle

terms = []
doc_dict = {}
inverted_index = {}
stopwords = ['the', 'is', 'at', 'of', 'on', 'and', 'a']


def read_file(in_file):
    """extract the document number and document text, store in a dictionary"""
    cur_doc_name = ''
    cur_doc_text = ''
    doc_start = re.compile(r'<DOC \d+>', re.I)

    while 1:
        line = in_file.readline()
        if line == '':  # EOF
            in_file.close()
            break
        if line == '\r\n' or line == '\n':  # new-line
            continue

        if '</DOC>' in line:  # end of current document
            doc_dict[int(cur_doc_name)] = cur_doc_text
            cur_doc_text = ''
        elif doc_start.match(line) is not None:  # start of current document
            cur_doc_name = doc_start.match(line).group(0)[5:-1]
        else:
            cur_doc_text += line


def text_process():
    """process each document text (tokenize, lowercase, stemming and remove stopwords) and store as a set"""
    document_ids = doc_dict.keys()
    for doc_id in document_ids:
        document = doc_dict[doc_id]
        document = re.sub(r'\W', ' ', document)  # remove non-alphanumeric (or r'[^a-zA-Z0-9_]'
        stemmer = nltk.PorterStemmer()  # Porter Stemmer
        words = document.split()
        length = len(words)
        for index in range(0, length):
            word = words[index]
            word = word.lower()  # lowercase
            word = stemmer.stem(word)  # stem
            words[index] = word
        words = [word for word in words if word not in stopwords]  # remove stopwords
        words = list(set(words))  # set of words
        doc_dict[doc_id] = words
    #print_dict(doc_dict)


def print_dict(dictionary, *args):
    """helper function - print dictionary with given key order, if any"""
    if len(args) > 0:
        keys = args[0]
    else:
        keys = dictionary.keys()
    for key in keys:
        print key
        print dictionary[key]


def write_dict(dictionary, file_name, *args):
    """helper function - write dictionary with given key order, if any"""
    out_f = open(file_name, 'w')
    if len(args) > 0:
        keys = args[0]
    else:
        keys = dictionary.keys()
    for key in keys:
        out_f.write(key + ': ')
        pl = dictionary[key]
        out_f.write('[' + str(pl[0]))
        out_f.write(' -> [' + ','.join(str(e) for e in pl[1]) + ']]\n')
    out_f.close()


def construct_inverted_index():
    """find terms, document frequency and its posting list"""
    for key, value in doc_dict.iteritems():
        for item in value:
            if item in inverted_index:  # type existed
                inverted_index[item].append(key)
            else:
                inverted_index[item] = [key]  # new type
    # sort terms and posting lists, record document frequency
    types = inverted_index.keys()
    types.sort()
    for term in types:
        sorted_list = inverted_index[term]
        sorted_list.sort()
        inverted_index[term] = [len(sorted_list), sorted_list]
    write_dict(inverted_index, 'inverted_index.txt', types)
    pickle.dump(inverted_index, open("inverted_index.p", "wb"))


def main():
    in_file = open('documents.txt', 'r')
    read_file(in_file)
    text_process()
    construct_inverted_index()


if __name__ == "__main__":
    main()
