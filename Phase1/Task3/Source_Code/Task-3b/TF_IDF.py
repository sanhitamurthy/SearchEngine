import os
import math


final_query_text="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/Source_Code/Task-3b/cacm_stemquery.txt"
top_tfidf_files="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/output/stemmed/TFIDF_Task3b.txt"
clean_corpus="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/stemmed_files/"

N=len(os.listdir(clean_corpus))

def unigram(invertedList):
    for filename in os.listdir(clean_corpus):
        folder=open(clean_corpus+filename)
        open_file = folder.read()
        open_file=open_file.split(" ")
        filename=filename[:-4]
        length=len(open_file)
        for i in range(length):
            token = open_file[i]
            invertedList = calculate_index(token, filename, invertedList)
    return invertedList


def calculate_index(token,filename,invertedList):
    if token not in invertedList:
        freq = {filename:1}
        invertedList.update({token:freq})
    elif filename in invertedList[token]:
        invertedList[token][filename] = invertedList[token][filename] + 1
    else:
        invertedList[token].update({filename:1})
    return invertedList

def calc_tfidf_score(term_freq,document,invertedList,document_length):
    term_frequency=invertedList[term_freq][document]/document_length[document]
    inverse_doc_freq=1.0+(math.log(N/(invertedList[term_freq][document]+1.0)))
    return term_frequency,inverse_doc_freq


def calc_doc_len():
    document_len = {}
    for filename in os.listdir(clean_corpus):
        folder=open(clean_corpus+filename).read()
        document_len[filename[:-4]]=len(folder.split())
    return document_len



def tfidf_calculation(invertedList,document_length):
    tfidf_score_dict={}
    for each_entry,value in invertedList.items():
        tfidf_score_dict[each_entry]={}

        for document in invertedList[each_entry]:
            term_freq,inverse_doc_freq=calc_tfidf_score(each_entry,document,invertedList,document_length)
            # inverse_doc_freq = calc_tfidf_score(each_entry, invertedList[i], invertedList, document_length)[1]
            tfidf_score_dict[each_entry][document]=term_freq*inverse_doc_freq

    return tfidf_score_dict



def process_query(all_content):
    folder=open(all_content,'r').read()
    folder=folder.splitlines()
    all_query_terms = []
    for each_entry in folder:
        all_query_terms.append(each_entry.split())
    return all_query_terms

def calc_document_score(document,dict_tfidf):
    total=0
    for each_entry in dict_tfidf:
        entries=dict_tfidf[each_entry]
        if document in entries:
            tfidf_value=dict_tfidf[each_entry][document]
            total= total+tfidf_value
    return total


def fetch_score_for_document(all_queries,tfidf_score):
    index_of_queries={}
    score_list_document={}
    for each_entry in all_queries:
        if each_entry not in tfidf_score:
            index_of_queries[each_entry] = {}
        else:
            index_of_queries[each_entry] = tfidf_score[each_entry]

    for each_entry in index_of_queries:
        index_of_entries=index_of_queries[each_entry]
        for each_document in index_of_entries:
            if each_document not in score_list_document:
                scores=calc_document_score(each_document,index_of_queries)
                score_list_document[each_document]=scores
    return score_list_document


def write_function(all_query,TFIDF_value):
    query_id=1
    writing_file=open(top_tfidf_files,"w")
    j=0
    while j< len(all_query):
        TFIDF_scores=fetch_score_for_document(all_query[j],TFIDF_value)
        sortedList=sorted(TFIDF_scores.items(), key=lambda x:x[1], reverse=True)
        i=0
        while i< 100:
            writing_file.write(str(query_id) + " "+"Q0" + " " + str(sortedList[i][0]) + " " + str(i+1) + " " + str(sortedList[i][1]) + " " + "TFIDF" + "\n")
            i+=1
        j+=1

        print(" query "+str(query_id)+" finished")
        query_id+=1
    writing_file.close()

if __name__ == '__main__':
    main()

def main():
    print("Running TFIDF")
    invertedList1={}
    invertedList=unigram(invertedList1)
    doc_length=calc_doc_len()
    TFIDF_value=tfidf_calculation(invertedList,doc_length)
    all_queries=process_query(final_query_text)
    write_function(all_queries,TFIDF_value)
