#################################################################################################
# This script use inverted index to evaluate conjunctive query.
# Note: can only process conjunctive queries with two operands
# To run:
#   python evaluate_query.py
#################################################################################################

from nltk import PorterStemmer
import pickle


def intersect(pl1, pl2):
    """intersect two posting lists"""
    result = []
    if pl1 is None or pl2 is None:
        return result
    i, j = 0, 0
    length1, length2, l1, l2 = pl1[0], pl2[0], pl1[1], pl2[1]
    while i < length1 and j < length2:
        if l1[i] == l2[j]:
            result.append(l1[i])
            i += 1
            j += 1
        elif l1[i] < l2[j]:
            i += 1
        else:
            j += 1
    return result


def main():
    inverted_index = pickle.load(open("inverted_index.p", "rb"))
    out_f = open('query_result.txt', 'w')
    stemmer = PorterStemmer()
    queries = ["asus AND google", "screen AND bad", "great AND tablet"]
    for query in queries:
        words = query.split()
        term1, term2 = stemmer.stem(words[0]), stemmer.stem(words[-1])
        out_f.write(query + ': ')
        result = intersect(inverted_index[term1], inverted_index[term2])
        out_f.write('[' + ', '.join(str(e) for e in result) + ']\n')
        print query
        print intersect(inverted_index[term1], inverted_index[term2])


if __name__ == "__main__":
    main()
