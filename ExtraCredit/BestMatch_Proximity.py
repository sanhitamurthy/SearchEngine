import operator
import os
import re
import shutil
from collections import defaultdict
from glob import glob
from itertools import product
from math import log

# Global Constants
k1 = 1.2
k2 = 100
b = 0.75
query_map = {}
query_id = 1
relevant_doc_map = {}
docCollectionPath = "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"

# Parameters for BM25 calculation
CURRENT_DIRECTORY = os.getcwd ()
QUERY_ID = 0


# Function to build inverted index from corpus
def build_index ():
    corpus_inverted_index = {}
    corpus_positional_inverted_index = {}
    word_count = {}
    path = os.path.join (docCollectionPath, '*.txt')
    for file in glob (path):
        doc = open (file, 'r')
        doc_id = os.path.basename (file)
        word_count[doc_id] = 0
        for terms in doc.readlines ():
            terms = terms.split ()
            for i in range (len (terms)):
                if terms[i] == '':
                    continue
                word_count[doc_id] += 1
                term = terms[i]
                if term not in corpus_inverted_index.keys ():
                    doc_term_freq = {doc_id: 1}
                    corpus_inverted_index[term] = doc_term_freq
                elif doc_id not in corpus_inverted_index[term].keys ():
                    corpus_inverted_index[term][doc_id] = 1
                else:
                    corpus_inverted_index[term][doc_id] += 1

                # Positional inverted index.
                if term not in corpus_positional_inverted_index.keys ():
                    doc_term_pos = {doc_id: [i]}
                    corpus_positional_inverted_index[term] = doc_term_pos
                elif doc_id not in corpus_positional_inverted_index[term].keys ():
                    corpus_positional_inverted_index[term][doc_id] = [i]
                else:
                    corpus_positional_inverted_index[term][doc_id].append (i)
    return corpus_positional_inverted_index


def get_proximity_matched_documents (query_words, corpus_positional_inverted_index, slider):
    doc_list = []
    term_list = []
    combined_list = []

    for word in query_words:
        if word in corpus_positional_inverted_index:
            doc_list.append ({word: corpus_positional_inverted_index[word]})
            term_list.append (corpus_positional_inverted_index[word])
        else:
            term_list.append ({})

    combine_query_word_dict = defaultdict (list)
    relevant_documents = set ().union (*term_list)
    # print (" The set is : " + str (s))
    for key in relevant_documents:
        for entry in term_list:
            if entry is not None:
                if entry.get (key) is not None:
                    if key in combine_query_word_dict.keys ():
                        combine_query_word_dict[key].append (entry.get (key))
                    else:
                        combine_query_word_dict[key] = [entry.get (key)]

    common_query_docs = {}
    for k, v in combine_query_word_dict.items ():
        if len (v) == 1:
            common_query_docs[k] = v
        if len (v) > 1:
            temp = list (list (product (*v)))
            common_query_docs[k] = temp
    # print ("The common query docs is : " + str (common_query_docs))

    # are the terms in proximity?
    for k, v in common_query_docs.items ():
        for pos_list in v:
            if isinstance (pos_list, list):
                combined_list.append (k)
            else:
                val_len = len (pos_list)
                for i in range (val_len - 1):
                    if pos_list[i + 1] - pos_list[i] < slider:
                        combined_list.append (k)
    return relevant_documents


# BM25 calculation
def generate_index ():
    doc_name = {}  # mapping doc name and ids
    doc_length = {}  # mapping the length and the doc_id
    inverted_index = {}
    counter = 1
    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'relevant_clean_corpus_bm_proximity')
    # num_of_files = len (glob (os.path.join (INPUT_FOLDER, '*.txt')))
    for file in glob (os.path.join (path, '*.txt')):
        head, tail = os.path.split (file)
        file_key = tail.split (".")[0]
        # print ("The file name is " + str (file))
        doc_name.update ({counter: file_key})
        doc_id = counter
        doc = open (file, 'r').read ()
        doc_length.update ({doc_id: len (doc.split ())})
        for term in doc.split ():
            if term not in inverted_index.keys ():
                doc_term_freq = {doc_id: 1}
                inverted_index.update ({term: doc_term_freq})
            elif doc_id not in inverted_index[term].keys ():
                inverted_index[term].update ({doc_id: 1})
            else:
                inverted_index[term][doc_id] += 1
        counter += 1
    total_num_of_docs = counter - 1
    # print (" The docmap is " + str (doc_name))
    return inverted_index, total_num_of_docs, doc_name, doc_length


def generate_doc_bm25_score (query, inverted_index, total_num_of_docs, relevant_list, doc_name, doc_length):
    query_term_freq = {}
    query_term_list = query.split ()
    # print ("The query term list is " + str (query_term_list))
    reduced_inverted_index = {}  # this inverted_index contains only those terms which are present in query
    for term in query_term_list:
        if term not in query_term_freq.keys ():
            query_term_freq.update ({term: 1})
        else:
            query_term_freq[term] += 1
    # reducing the inverted_index with only required terms in query
    for term in query_term_freq:
        if term in inverted_index.keys ():
            reduced_inverted_index.update ({term: inverted_index[term]})
        else:
            reduced_inverted_index.update ({term: {}})
    process_score (query_term_freq, reduced_inverted_index, total_num_of_docs, relevant_list, doc_name, doc_length)


def get_relevant_numb (doc_list, relevant_list):
    counter = 0
    for doc_id in doc_list:
        if doc_id in relevant_list:
            counter += 1
    return counter


def calculate_BM25 (n, f, qf, r, N, dl, R, doc_length):
    AVDL = generate_avdl (doc_length)
    k1 = 1.2
    k2 = 100
    b = 0.75
    K = k1 * ((1 - b) + b * (float (dl) / float (AVDL)))
    first = log (((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    return first * second * third


def process_score (query_term, inverted_index, N, relevant_list, doc_name, doc_length):
    doc_score = {}
    R = len (relevant_list)
    for term in inverted_index:  # inverted_index.keys() and query_term.keys() are same
        n = len (inverted_index[term])
        dl = 0
        qf = query_term[term]
        r = get_relevant_numb (inverted_index[term], relevant_list)
        for doc_id in inverted_index[term]:
            f = inverted_index[term][doc_id]
            if doc_id in doc_length.keys ():
                dl = doc_length[doc_id]
            score = calculate_BM25 (n, f, qf, r, N, dl, R, doc_length)
            if doc_id in doc_score:
                total_score = doc_score[doc_id] + score
                doc_score.update ({doc_id: total_score})
            else:
                doc_score.update ({doc_id: score})
    sorted_doc_score = sorted (doc_score.items (), key=operator.itemgetter (1), reverse=True)
    # print (" The sorted doc_score is " + str (sorted_doc_score))
    write_doc_score (sorted_doc_score, doc_name)


def write_doc_score (sorted_doc_score, doc_name):
    if (len (sorted_doc_score) > 0):
        out_file = open ("Relevant_doc_bestMatch_proximity.txt", 'a')
        # print (" The outfile is " + str (out_file))
        for i in range (min (100, len (sorted_doc_score))):
            doc_id, doc_score = sorted_doc_score[i]
            out_file.write (str (QUERY_ID) + " Q0 " + doc_name[doc_id] + " " + str (i + 1) + " " + str (
                doc_score) + " BM25_Model\n")
        out_file.close ()
        print
        "\nDocument Scoring for Query id = " + str (QUERY_ID) + " has been generated inside BM25_doc_score.txt"
    else:
        print
        "\nTerm not found in the corpus"


def get_relevant_list (doc_name):
    file_list = []
    rel_doc_id = []
    rel_file = open ('/Users/dipanjan/gitHub/Python-Projects/FinalProject/test-collection/cacm.rel.txt', 'r')
    for line in rel_file.readlines ():
        params = line.split ()
        if params and (params[0] == str (QUERY_ID)):
            file_list.append (params[2])
    for doc_id in doc_name:
        if doc_name[doc_id] in file_list:
            rel_doc_id.append (doc_id)
    rel_file.close ()
    return rel_doc_id


def generate_avdl (doc_length):
    sum = 0
    for doc_id in doc_length:
        sum += doc_length[doc_id]
    return (float (sum) / float (len (doc_length)))


## End of BM25 calculation

def main ():
    docCollectionPath = "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"
    corpus_positional_inverted_index = build_index ()
    queryFile = "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/query2.txt"
    slider = 5
    # method to extract the queries and populate the dictionary with document details
    QueryLines = [line.rstrip ('\n') for line in open (queryFile)]
    query_id = 1
    for eachLine in QueryLines:
        wordList = re.split ('\W+', eachLine)
        while '' in wordList:
            wordList.remove ('')
        wordsInLowerCase = []
        for word in wordList:
            wordsInLowerCase.append (word.lower ())
            # print (str (wordsInLowerCase))
        ordered_proximity_match = list (
            get_proximity_matched_documents (wordsInLowerCase, corpus_positional_inverted_index, slider))
        # print(str(ordered_proximity_match))
        if not ordered_proximity_match:
            print ("There are no relevant documents for the query no : " +str(query_id))
        query_map[query_id] = wordsInLowerCase
        # print ("The relevant doc_list is " + str (ordered_proximity_match))
        relevant_doc_map[query_id] = ordered_proximity_match
        query_id = query_id + 1
    # print ("The relevant doc_map is " + str (relevant_doc_map))
    # print ("The query map is " + str (query_map))

    for key in relevant_doc_map.keys ():
        query_term_list = query_map[key]
        query = ""
        for term in query_term_list:
            query += term + " "
        query_file = open ("queryFile.txt", "w")
        query_file.write (query)
        # print ("The reconstructed query is " + query)
        doc_list = relevant_doc_map.get (key)
        # print(" The doc_list is " +str(doc_list))
        shutil.rmtree ('relevant_clean_corpus_bm_proximity', ignore_errors=True)
        os.mkdir ('relevant_clean_corpus_bm_proximity')
        for entry in doc_list:
            filename = entry
            # print ("The filename is " + str (filename))
            # print(os.path.join (docCollectionPath, filename))
            shutil.copy2 (os.path.join (docCollectionPath, filename), 'relevant_clean_corpus_bm_proximity')
        inputfolder = os.path.join (os.getcwd (), 'relevant_clean_corpus_bm_proximity')
        inputqueryfile = os.path.join (os.getcwd (), 'queryFile.txt')
        global QUERY_ID
        inverted_index, total_num_of_docs, doc_name, doc_length = generate_index ()
        # Removing the existing VSM_doc_score.txt to prevent appending the new results with the old one.
        query_file = open ("queryFile.txt", 'r')
        for query in query_file.readlines ():
            QUERY_ID += 1
            relevant_list = get_relevant_list (doc_name)
            generate_doc_bm25_score (query, inverted_index, total_num_of_docs, relevant_list, doc_name, doc_length)


if __name__ == '__main__':
    main ()
