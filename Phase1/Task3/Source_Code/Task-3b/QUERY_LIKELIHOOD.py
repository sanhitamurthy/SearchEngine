import os
import math


final_query_text="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/Source_Code/Task-3b/cacm_stemquery.txt"
top_ql_files="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/output/stemmed/QL_Task3b.txt"
clean_corpus="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/stemmed_files/"
cacm_rel_path="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/test-collection/test-collection/cacm.rel.txt"



k1=1.2
k2=100
b=0.75
alpha=1
beta=0.75
gamma=0.15
LAMBDA=0.35
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


def calc_doc_len():
    document_len = {}
    for filename in os.listdir(clean_corpus):
        folder=open(clean_corpus+filename).read()
        document_len[filename[:-4]]=len(folder.split())
    return document_len

def extract_queries(query_file):
    filename = open(query_file,'r')
    all_content=[]
    for each_entry in filename:
        each_entry=" ".join(each_entry.split())
        each_entry=each_entry.strip()
        last_word=each_entry[-1]
        space=' '
        newLine='\n'
        if last_word == newLine:
            all_content.append(each_entry[:-1])
        elif last_word == space:
            all_content.append(each_entry[:-1])
        else:
            all_content.append(each_entry)
    return all_content


def process_query(all_content):
    all_query_terms = {}
    i=0
    while i< len(all_content):
        term=all_content[i]
        all_query_terms[term] = term.split()
        i+=1
    return all_query_terms

def calc_QL_score(result,collection,index,all_queries,unique_docs,doc_lengths):
    query_id=-1
    total_scores=0
    query_terms=process_query(all_queries)

    for each_entry in all_queries:
        query_id=query_id+1
        document_ranks={}
        for entry in unique_docs:
            list_of_query_terms=list(set(query_terms[each_entry]))
            j=0
            while j<len(list_of_query_terms):
                each_term=list_of_query_terms[j]
                if each_term in index:
                    each_term_in_index=index[each_term]
                    if entry not in each_term_in_index:
                        document_term_weights = 0
                    else:
                        document_term_weights = each_term_in_index[entry]
                    query_frequency_by_doc=document_term_weights/doc_lengths[entry]
                    term_index_by_collection=sum(each_term_in_index.values())/collection
                    term1=((1-LAMBDA)*query_frequency_by_doc)
                    term2=(LAMBDA*term_index_by_collection)
                    score=math.log(term1+term2)
                    total_scores=total_scores+score
                j+=1
            document_ranks[entry]=total_scores
            total_scores=0
        rank_documents(document_ranks,query_id,result)

def rank_documents(document_ranks,query_id,result):
    writing_file = open(top_ql_files, "a")
    sortedList = sorted(document_ranks, key=document_ranks.__getitem__)
    start=-(result)
    top_res=sortedList[start:]
    top_res.reverse()
    doc_rank=0
    i=0
    while i< len(top_res):
        doc_rank+=1
        writing_file.write(str(query_id+1) + " " + "Q0" + " " + str(top_res[i]) + " " + str(doc_rank) + " " + str(
            document_ranks[top_res[i]]) + " " + "QueryLikelihood" + "\n")
        i+=1


def main():
    print("Running QL")
    invertedList1={}
    index=unigram(invertedList1)
    unique_docs=[file[:-4] for file in os.listdir(clean_corpus)]
    docLength=calc_doc_len()
    querySet=extract_queries(final_query_text)
    collection=sum(docLength.values())
    calc_QL_score(100,collection,index,querySet,unique_docs,docLength)


if __name__ == '__main__':
    main()
