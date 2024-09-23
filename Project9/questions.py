import nltk
import sys
import os
import string
from numpy import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    Dictionary = {}
    TextFiles = os.listdir(directory)
    for file in TextFiles:
        path = directory + os.sep + file
        f = open(f"{path}", 'r', encoding="utf-8")
        Contents = ''
        for line in f:
            Contents += line
        f.close()
        Dictionary[file] = Contents
    return Dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    RevisedList = []
    document = document.lower()
    WordList = nltk.tokenize.word_tokenize(document)
    for word in WordList:
        if word in string.punctuation:
            continue
        if word in nltk.corpus.stopwords.words("english"):
            continue
        RevisedList.append(word)
    return RevisedList


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_to_value = {}
    no_of_documents = len(documents)
    for doc in documents:
        WordList = documents[doc]
        for word in WordList:
            if word in word_to_value:
                continue
            count = 0
            for doc2 in documents:
                if word in documents[doc2]:
                    count += 1
            word_to_value[word] = log(no_of_documents/count)
    return word_to_value


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    FileList = []
    for file in files:
        Words = files[file]
        Total = 0
        for word in query:
            if word not in Words:
                continue
            Count = Words.count(word)
            tf_idf = Count * idfs[word]
            Total += tf_idf
        Tuple = (file, Total)
        FileList.append(Tuple)
    FileList = sorted(FileList, key=lambda i: -i[1])
    TopFiles = []
    for j in range(len(FileList)):
        TopFiles.append(FileList[j][0])
    return TopFiles[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    SentenceList =[]
    for sentence in sentences:
        Words = sentences[sentence]
        Count = 0
        Total = 0
        for word in query:
            if word not in Words:
                continue
            Occurences = Words.count(word)
            Count += Occurences
            idf = idfs[word]
            Total += idf
        density = Count / len(Words)
        Tuple = (sentence, Total, density)
        SentenceList.append(Tuple)
    SentenceList = sorted(SentenceList, key=lambda x: (-x[1], -x[2]))
    TopSentences = []
    for k in range(len(SentenceList)):
        TopSentences.append(SentenceList[k][0])
    return TopSentences[:n]


if __name__ == "__main__":
    main()
