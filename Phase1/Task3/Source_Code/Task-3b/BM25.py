import os
import math


final_query_text="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/Source_Code/Task-3b/cacm_stemquery.txt"
top_bm25_files="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/output/stemmed/BM25_Task3b.txt"
clean_corpus="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/stemmed_files/"
cacm_rel_path="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/test-collection/test-collection/cacm.rel.txt"


k1=1.2
k2=100
b=0.75
alpha=1
beta=0.75
gamma=0.15
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

def extract_queries(filename):
    all_content=[]
    filename=open(filename)
    lines=filename.read()
    lines=lines.splitlines()
    for line in lines:
        all_content.append(line.split())
    return all_content

def calc_query_freq(query_term,invertedList):
    query_frequency={}
    i=0
    while i < len(query_term):
        if query_term[i] not in query_frequency:
            query_frequency[query_term[i]] =1
        else:
            query_frequency[query_term[i]]=query_frequency[query_term[i]]+1
        i += 1
    for each_entry in invertedList:
        if each_entry not in query_frequency:
            query_frequency[each_entry]=0
    return query_frequency


def calc_doc_len():
    document_len = {}
    for filename in os.listdir(clean_corpus):
        folder=open(clean_corpus+filename).read()
        document_len[filename[:-4]]=len(folder.split())
    return document_len


def averageDocLen(document_len):
    totalNum=0
    for key in document_len:
        file_entry_value=document_len[key]
        totalNum = totalNum + file_entry_value
    avg=totalNum/N
    return avg


def BM25_score_calc(n, doc_freq, query_freq, r, N, doc_len, avg_doc_len,R):
    r=0
    R=0
    numerator = float(doc_len)
    denominator = float(avg_doc_len)
    division_const = numerator / denominator
    K = k1 * ((1 - b) + b * division_const)
    term1 = math.log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    term2 = ((k1 + 1) * doc_freq) / (K + doc_freq)
    term3 = ((k2 + 1) * query_freq) / (k2 + query_freq)
    return term1 * term2 * term3



def fetch_relevant_documents(query_id,document_list):
    filename = open(cacm_rel_path).read()
    filename=filename.splitlines()
    list_relevant=[]
    relevant_docs=[]
    i=0
    while i <len(filename):
        if filename[i].split()[0]==str(query_id):
            list_relevant.append(filename[i].split()[2])
        i+=1
    for every_document in document_list:
        if every_document in list_relevant:
            relevant_docs.append(every_document)
    return relevant_docs


def find_all_documents_for_query(newQuery,invertedList,docLengths,query_id):
    BM25scorelist = {}
    query_freq=calc_query_freq(newQuery,invertedList)
    avdl=averageDocLen(docLengths)
    for every_entry in docLengths.keys():
        BM25scorelist[every_entry]=0
    relevantList=fetch_relevant_documents(query_id,docLengths)
    for each_entry in newQuery:
        if each_entry in invertedList:
            document_dictionary=invertedList[each_entry]
            totalNum = 0
            # for every_document in invertedList[each_entry]:
            #     if every_document in relevantList:
            #         totalNum = totalNum + 1
            for doc in document_dictionary:
                BM25=BM25_score_calc(len(document_dictionary),document_dictionary[doc],query_freq[each_entry],0,len(docLengths.keys()),docLengths[doc],avdl,0)
                BM25scorelist[doc] = BM25scorelist[doc]+BM25
    return BM25scorelist

def write_function(all_query,inveredList,docLengths):
    query_id=1
    writing_file=open(top_bm25_files,"w")
    j=0
    while j< len(all_query):
        BM25_score=find_all_documents_for_query(all_query[j],inveredList,docLengths,query_id)
        sortedList=sorted(BM25_score.items(), key=lambda x:x[1], reverse=True)
        i=0
        while i< 100:
            writing_file.write(str(query_id) + " "+"Q0" + " " + str(sortedList[i][0]) + " " + str(i+1) + " " + str(sortedList[i][1]) + " " + "BM25" + "\n")
            i+=1
        j+=1

        print(" query "+str(query_id)+" finished")
        query_id+=1
    writing_file.close()

def main():
    all_queries=extract_queries(final_query_text)
    invertedIndex={}
    invertedList=unigram(invertedIndex)
    doc_lengths=calc_doc_len()
    write_function(all_queries,invertedList,doc_lengths)


if __name__ == '__main__':
    main()
