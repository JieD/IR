#################################################################################################
# This script creates an inverted index for a given input file (containing multiple documents).
#
# Command line arguments:
# [input]  - a txt file containing all the documents
# input:  documents.txt
#
# usage: #python inverted_index.py [input]
#################################################################################################

import sys
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
    """process each document text - tokenize, lowercase, stemming and remove stopwords"""
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
    print_dict(doc_dict)


def print_dict(dictionary, *args):
    """helper function - print dictionary with given key order, if any"""
    if len(args) > 0:
        keys = args[0]
    else:
        keys = dictionary.keys()
    for key in keys:
        print key
        print dictionary[key]


def construct_inverted_index():
    """find terms and its posting lists"""
    for key, value in doc_dict.iteritems():
        for item in value:
            if item in inverted_index:
                inverted_index[item].append(key)
            else:
                inverted_index[item] = [key]
    # sort terms and posting lists, record document frequency
    types = inverted_index.keys()
    types.sort()
    for term in types:
        sorted_list = inverted_index[term]
        sorted_list.sort()
        inverted_index[term] = [len(sorted_list), sorted_list]
    print_dict(inverted_index, types)
    pickle.dump(inverted_index, open("inverted_index.p", "wb"))


def main():
    # load command line arguments
    if len(sys.argv) is not 2:
        print 'incorrect arguments\nneed: input.txt'
        sys.exit(2)
    else:
        file_name = sys.argv[1]
    in_file = open(file_name, 'r')

    read_file(in_file)
    text_process()
    construct_inverted_index()


if __name__ == "__main__":
    main()
