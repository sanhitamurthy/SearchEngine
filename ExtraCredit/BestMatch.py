import glob
import operator
import os
import re
import shutil
from math import log

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMap = {}
finalList = []
query_map = {}
relevent_doc_map = {}
query_id = 1

# Parameters for BM25 calculation
CURRENT_DIRECTORY = os.getcwd ()
QUERY_ID = 0


def buildIndex (path):
    docId = 1
    fileList = [f for f in os.listdir (path) if os.path.isfile (os.path.join (path, f))]
    fileobj = open ('frequency.txt', 'w')
    for eachFile in fileList:
        position = 1
        count = 0
        # docName = "Doc_Id_" + str(docId)
        # docName =  str(docId)
        docIdMap[docId] = eachFile
        lines = [line.rstrip ('\n') for line in open (path + "/" + eachFile)]

        for eachLine in lines:
            wordList = re.split ('\W+', eachLine)

            while '' in wordList:
                wordList.remove ('')
            for word in wordList:
                if (word.lower () in dictionary):
                    postingList = dictionary[word.lower ()]
                    if (docId in postingList):
                        postingList[docId].append (position)
                        position = position + 1
                    else:
                        postingList[docId] = [position]
                        position = position + 1
                else:
                    dictionary[word.lower ()] = {docId: [position]}
                    position = position + 1
        docId = docId + 1


def print_dict ():
    # function to print the terms and posting list in the index
    fileobj = open ("invertedIndex.txt", 'w')
    for key in dictionary.keys ():
        print (key + " --> " + str (dictionary[key]))
        fileobj.write (key + " --> " + str (dictionary[key]))
        fileobj.write ("\n")
    fileobj.close ()


def print_doc_list ():
    for key in docIdMap:
        print ("Doc ID: " + str (key) + " ==> " + str (docIdMap[key]))


def getRelevantDocuments (relevent_doc_map):
    for entry in relevent_doc_map.keys ():
        doc_list = []
        doc_list = relevent_doc_map.get (entry)

        for i in range (0, len (doc_list)):
            value = doc_list[i]
            doc_name = docIdMap.get (value)
            doc_list[i] = doc_name
        relevent_doc_map[entry] = doc_list
    return relevent_doc_map


def getalldocuments (query):
    result = []
    for term in query:
        if getPostingList (term) is not None:
            result += getPostingList (term)
    return list (set (result))


def getPostingList (term):
    if term in dictionary.keys ():
        postingList = dictionary[term]
        # print("The term is : " + str(term) + " => and posting list is : " +str(postingList))
        keysList = []
        for keys in postingList:
            keysList.append (keys)
        keysList.sort ()
        # print ("The keysList is : " +str(keysList))
        return keysList
    else:
        return None

def best_match_retrival (query, query_id):
    all_docs = getalldocuments (query)
    if all_docs is not None:
        relevent_doc_map[query_id] = all_docs
    else:
        print ("There are no documents in the corpus for the given query")


# BM25 calculation

def generate_relevant_doc_index ():
    doc_name = {}  # mapping doc name and ids
    doc_length = {}  # mapping doc_id and doc_length
    inverted_index = {}
    counter = 1
    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'relevant_clean_corpus_bestMatch')
    # num_of_files = len (glob (os.path.join (INPUT_FOLDER, '*.txt')))
    for file in glob.glob (os.path.join (path, '*.txt')):
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
    query_term_inverted_index = {}  # map for inverted_index present in query
    for term in query_term_list:
        if term not in query_term_freq.keys ():
            query_term_freq.update ({term: 1})
        else:
            query_term_freq[term] += 1
    # reducing the inverted_index with only required terms in query
    for term in query_term_freq:
        if term in inverted_index.keys ():
            query_term_inverted_index.update ({term: inverted_index[term]})
        else:
            query_term_inverted_index.update ({term: {}})
    process_score (query_term_freq, query_term_inverted_index, total_num_of_docs, relevant_list, doc_name, doc_length)


def get_relevant_numb (doc_list, relevant_list):
    counter = 0
    for doc_id in doc_list:
        if doc_id in relevant_list:
            counter += 1
    return counter


def calculate_BM25 (n, f, qf, r, N, dl, R, doc_length):
    AVDL = compute_avdl (doc_length)
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
        out_file = open ("Relevant_doc_bestmatch.txt", 'a')
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


def compute_avdl (doc_length):
    sum = 0
    for doc_id in doc_length:
        sum += doc_length[doc_id]
    return (float (sum) / float (len (doc_length)))


## End of BM25 calculation

def main ():
    # docCollectionPath = input("Enter path of text file collection : ")
    docCollectionPath = "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"
    # queryFile = input("Enter path of query file : ")
    queryFile = "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/query2.txt"
    # method to build the index
    buildIndex (docCollectionPath)

    # print ("")
    # print ("Inverted Index :")
    # print_dict ()
    # print ("")
    # print ("Document List :")
    # print_doc_list ()
    # print ("")

    # method to extract the queries and populate the dictionary with document details
    QueryLines = [line.rstrip ('\n') for line in open (queryFile)]
    for eachLine in QueryLines:
        wordList = re.split ('\W+', eachLine)

        while '' in wordList:
            wordList.remove ('')

        wordsInLowerCase = []
        for word in wordList:
            global query_id
            wordsInLowerCase.append (word.lower ())
            # print(str(wordsInLowerCase))
        best_match_retrival (wordsInLowerCase, query_id)
        query_map[query_id] = wordsInLowerCase
        query_id = query_id + 1

    # Ranking by relevance
    relevant_documents = getRelevantDocuments (relevent_doc_map)
    # print(str(relevant_documents))
    for key, value in relevant_documents.items ():
        if not relevant_documents[key]:
            print ("There are no relevant documents for the query no: " + str(key) + "  in corpus")
    # print ("The relevant document list  is : " + str (relevant_documents))
    # copy the relevant documents to input folder for BM25
    for key in relevent_doc_map.keys ():
        # print (" I am here")
        query_term_list = query_map[key]
        query = ""
        for term in query_term_list:
            query += term + " "
        # print (" The query is " + str (query))
        query_file = open ("queryFile.txt", "w")
        query_file.write (query)
        # print ("The reconstructed query is " + query)
        doc_list = relevent_doc_map.get (key)
        # print ("The doc_list is " + str (doc_list))
        shutil.rmtree ('relevant_clean_corpus_bestMatch', ignore_errors=True)
        os.mkdir ('relevant_clean_corpus_bestMatch')
        for entry in doc_list:
            filename = entry
            # print ("The filename is " + str (filename))
            shutil.copy2 (os.path.join (docCollectionPath, filename), 'relevant_clean_corpus_bestMatch')
        inputfolder = os.path.join (os.getcwd (), 'relevant_clean_corpus_bestMatch')
        inputqueryfile = os.path.join (os.getcwd (), 'queryFile.txt')
        global QUERY_ID
        inverted_index, total_num_of_docs, doc_name, doc_length = generate_relevant_doc_index ()
        # Removing the existing VSM_doc_score.txt to prevent appending the new results with the old one.
        query_file = open ("queryFile.txt", 'r')
        for query in query_file.readlines ():
            QUERY_ID += 1
            relevant_list = get_relevant_list (doc_name)
            generate_doc_bm25_score (query, inverted_index, total_num_of_docs, relevant_list, doc_name, doc_length)


if __name__ == '__main__':
    main ()
