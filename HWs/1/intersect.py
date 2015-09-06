from nltk import PorterStemmer
import pickle


def intersect(pl1, pl2):
    result = []
    if pl1 is None or pl2 is None:
        return result
    i, j = 0, 0
    while i < pl1[0] and j < pl2[0]:
        if pl1[1][i] == pl2[1][j]:
            result.append(pl1[1][i])
            i += 1
            j += 1
        elif pl1[1][i] < pl2[1][j]:
            i += 1
        else:
            j += 1
    return result

def process_query(query, inverted_index, stemmer):
    words = query.split()
    term1, term2 = stemmer.stem(words[0]), stemmer.stem(words[-1])
    print query, term1, term2
    return intersect(inverted_index[term1], inverted_index[term2])


def main():
    inverted_index = pickle.load(open("inverted_index.p", "rb"))
    stemmer = PorterStemmer()
    queries = ["asus AND google", "screen AND bad", "great AND tablet"]
    for query in queries:
        print process_query(query, inverted_index, stemmer)


if __name__ == "__main__":
    main()
