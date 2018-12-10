import os


source="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/test-collection/test-collection/common_words.txt"
clean_corpus_loc = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task1/Clean_Corpus1/"
result_corpus_loc= "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/stopped_corpus/"


def read(clean_corpus_loc):
    for file in os.listdir(clean_corpus_loc):
        filename=open(clean_corpus_loc+file)
        content= filename.readlines()
        all_stop_words=fetch_stop_words()
        stop_words_rem_content = perform_stopping(content,all_stop_words)
        write_content(stop_words_rem_content, file,result_corpus_loc)

def fetch_stop_words():
    filename = open(source)
    content = filename.readlines()
    return content

def perform_stopping(content,all_stop_words):
    final_result_content=[]
    final_stop_words=[]
    stopped_corpus_content=[]
    for every_entry in content:
        stopped_corpus_content.append(every_entry.strip())
    stopped_corpus_content=stopped_corpus_content[0].split(' ')
    for every_entry in all_stop_words:
        final_stop_words.append(every_entry.strip())
    i=0
    while i<len(stopped_corpus_content):
        if stopped_corpus_content[i] not in final_stop_words:
            final_result_content.append(stopped_corpus_content[i] )
        i+=1
    return final_result_content


def write_content(collection,filename, destination):
    folder = os.path.join(destination, filename)
    write_unigramCount_file = open(folder, "w")
    collection = ' '.join(collection)
    write_unigramCount_file.write(str(collection.encode(encoding='utf-8',errors='ignore')))


def main():
   read(clean_corpus_loc)
