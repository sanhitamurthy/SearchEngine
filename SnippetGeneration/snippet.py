import os
import re
import shutil

import dominate
from bs4 import BeautifulSoup
from dominate.tags import *

SNIPPET = 'snippets/'
RAW_HTML_PATH = '/Users/dipanjan/gitHub/GroupProject/FinalProject/test-collection/cacm/'
BM25_RES = '/Users/dipanjan/gitHub/GroupProject/FinalProject/BM25_Results/BM25.txt'
QUERY_PATH = '/Users/dipanjan/gitHub/GroupProject/FinalProject/test-collection/cacm.query.txt'
COMMON_WORD= '/Users/dipanjan/gitHub/GroupProject/FinalProject/test-collection/common_words'
WINDOW = 40

stop_word_list=[]


# get the top ranked documents from BM25 output and populate the dictionary
def getRanking ():
    BM25_rank_dict = {}
    BM25_file = open (BM25_RES, 'r')
    file_content = BM25_file.readlines ()
    for line in file_content:
        items = line.split (' ')
        queryID = int (items[0])
        if queryID in BM25_rank_dict:
            BM25_rank_dict[queryID].append (items[2])
        else:
            BM25_rank_dict[queryID] = [items[2]]  # items[2] contains docID
    return BM25_rank_dict


def processQuery ():
    processed_query_dict = {}
    raw_query_file = open (QUERY_PATH)
    html = BeautifulSoup (raw_query_file.read (), 'lxml')

    for doc in html.findAll ('doc'):
        docno = doc.find ('docno')
        queryID = int (docno.text)
        docno.decompose ()
        text = doc.text.strip ()
        processed_query_dict[queryID] = text
    #print("The processed query dict is " +str(processed_query_dict))
    return processed_query_dict


def startSnippetGeneration (ranked_document_list, processed_query_list):
    shutil.rmtree (SNIPPET, ignore_errors=True)
    os.mkdir (SNIPPET)
    for i in range (1, 65):
        createSnippet (processed_query_list[i], ranked_document_list[i], i)


def createSnippet (query, docList, queryID):
    cleanedQuery,query_original = clean (query)
    #print(cleanedQuery)
    newHtml = dominate.document (title=query_original)
    with newHtml.body:
        h1 (query_original)

    for docID in docList:

        filename = docID + '.html'
        path_ = 'file:///' + RAW_HTML_PATH + filename
        raw_html = open (RAW_HTML_PATH + filename)
        raw_html = BeautifulSoup (raw_html, 'lxml')
        text = raw_html.text.strip ()
        text = text.replace ('\t', ' ')
        text = re.sub (' +', ' ', text)
        lines = text.split ('\n')
        title = boldify (lines[0], cleanedQuery)
        originalBody = BeautifulSoup (' '.join (lines[1:]), 'lxml').text.strip ()
        bodyContent = originalBody.lower ().split (' ')
        queryTerms = query.lower ().split (' ')

        start = 0
        snippet = 0
        initialPos = 0
        snippetCount = len (bodyContent)
        while start < snippetCount - WINDOW:
            contentList = bodyContent[start:start + WINDOW]
            temp = 0
            for q in queryTerms:
                temp = temp + contentList.count (q)
            if temp > snippet:
                snippet = temp
                initialPos = start
            start = start + 1

        displaySnippet = boldify (' '.join (bodyContent[initialPos:initialPos + WINDOW] + ['...']), cleanedQuery)

        with newHtml.body:
            d = div ()
            with d:
                a (title, href=path_, style='text-decoration:none;font-size:14px')
                pre (path_, style='font-size:10px;color:brown;margin:0;padding:0')
                pre (displaySnippet, style='font-size:10px;color:black;margin:0;padding:0')
                br ()
                br ()

    file_ = open (SNIPPET + str (queryID) + '.html', 'w+')
    file_.write (str (newHtml))
    file_.close ()


def clean (query):
    stopped_query_list = []
    query = query.replace ('\t', ' ')
    query = re.sub (' +', ' ', query)
    query.replace ('\n', ' ')
    query_original=query
    pattern = re.compile ('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
    query = pattern.sub (' ', query)
    query_term_list=query.split(" ")
    for term in query_term_list:
         if term not in stop_word_list:
            stopped_query_list.append(term)
    # #print("The stopped query list is " +str(stopped_query_list))
    query = ""
    for term in stopped_query_list:
         query += term + " "
    # print ("The final query is : " + str (query))
    #print("The query is" +query)
    return query,query_original


def generate_stop_list():
    global stop_word_list
    with open(COMMON_WORD,'r') as f:
        stop_word_list =[line.strip() for line in f]
    return stop_word_list



def boldify (title, query):
    titleContents = title.split (' ')
    #print("Title content is " +str(titleContents))
    queryTerms = query.lower ().split (' ')
    #print ("query_terms is " + str (queryTerms))
    boldTerms = []
    for term in titleContents:
        if term.lower () in queryTerms:
            boldTerms.append (b (term))
        else:
            boldTerms.append (term)
    #print ("bold terms are  " + str (boldTerms))
    formatted_snippet = pre (style='margin:0;padding:0')
    count = 0
    for term in boldTerms:
        count += 1
        formatted_snippet.add (term)
        formatted_snippet.add (' ')
        if count % 15 == 0:
            formatted_snippet.add (br ())
    return formatted_snippet


def main ():
    ranked_document_list = getRanking ()  # get the ranked list from BM25 output
    processed_query_list = processQuery ()
    generate_stop_list()
    print ('\nStarted generating snippets')
    startSnippetGeneration (ranked_document_list, processed_query_list)
    print ('HTML output files with snippets are generated!')


if __name__ == "__main__":
    main ()
