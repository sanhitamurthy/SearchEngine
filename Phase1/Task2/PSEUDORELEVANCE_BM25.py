import os
import math
import re

relevant_list = {}
stop_words_list = []
final_corpus = {}

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0
r = 0.0
unigram_index = {}

path = "C:\\Users\\Ravi\\Desktop\\IR_ProjectRes\\Clean_Corpus1\\"

folder = open("C:/Users/Ravi/Documents/test-collection/cacm.rel.txt")
for entry in folder:
    all_content = entry.split()
    query_id = all_content[0]
    doc_id = all_content[2]
    if query_id in relevant_list:
        relevant_list[query_id].append(doc_id)
    else:
        relevant_list[query_id] = [doc_id]
folder.close()


def check_present(term, query_id):
    counter_value = 0
    query_id_str = str(query_id)
    if query_id_str in relevant_list:
        for each_query in relevant_list[query_id_str]:
            if len(each_query[5:]) < 4:
                if len(each_query[5:]) == 3:
                    each_query = each_query[0:5] + "0" + each_query[5:]
                elif len(each_query[5:]) == 2:
                    each_query = each_query[0:5] + "00" + each_query[5:]
                elif len(each_query[5:]) == 1:
                    each_query = each_query[0:5] + "000" + each_query[5:]
            filename = each_query + ".txt"
            file = open(path + filename, 'r')
            content = file.read()
            content = content.split()
            term = term.lower()
            if term in content:
                counter_value = counter_value + 1
    else:
        counter_value = 0
    return counter_value


def snippet_creation(file, query_text):
    file = open(path + file)
    content = file.read()
    new_content = content.lower().split("\n")
    all_snippets = {}
    for each_sentence in new_content:
        all_snippets[each_sentence] = get_significant_factor(each_sentence, query_text)
    keep_count = 1
    max_counter = 6
    summary = ""
    sortedList = sorted(all_snippets, key=all_snippets.get, reverse=True)
    for each_entry in sortedList:
        if keep_count < max_counter:
            str_each_entry = str(each_entry)
            summary = summary + " " + str_each_entry
            keep_count += 1
    return summary


def get_significant_factor(sentence, query):
    all_words = sentence.split()
    lower_value = 0
    higer_value = 0
    count_value = 0.0
    for each_entry in all_words:
        if boolean_check_present(each_entry, query):
            lower_value = all_words.index(each_entry)
            break
    length = len(all_words)
    start = length - 1
    mid = 0
    end = - 1
    for each_entry in range(start, mid, end):
        if boolean_check_present(all_words[each_entry], query):
            higer_value = each_entry
            break
    start_term = lower_value
    end_term = (higer_value + 1)
    for each_entry in all_words[start_term: end_term]:
        if boolean_check_present(each_entry, query):
            count_value = count_value + 1
    start = lower_value
    end = higer_value + 1
    sentence = all_words[start:end]
    if len(sentence) == 0:
        significance_factor = 0.0
    else:
        updated_count_value = count_value * count_value
        length = len(sentence)
        significance_factor = updated_count_value / length

    return significance_factor


def boolean_check_present(word, query_text):
    all_content = query_text.split()
    i = 0
    while i < len(all_content):
        if i == word:
            return True
        i += 1
    return False


def get_stop_list():
    folder = open("C:/Users/Ravi/Documents/test-collection/common_words.txt")
    for each_entry in folder:
        stop_words_list.append(each_entry.strip("\n"))
    folder.close()


def query_expansion_technique(topmost_docs, query_text):
    res_list = {}
    j = 0
    while j < len(topmost_docs):
        folder = open(path + topmost_docs[j], 'r')
        snippet = snippet_creation(topmost_docs[j], query_text)
        for each_entry in snippet.split():
            if each_entry in res_list:
                res_list[each_entry] += 1
            else:
                res_list[each_entry] = 1
        j += 1
        folder.close()


    terms = []
    value = 0
    totalDoc = 31
    sortedList = sorted(res_list, key=res_list.get, reverse=True)
    k = 0
    while k < len(sortedList):
        term = sortedList[k]
        lower_str = str(term).lower()
        if lower_str not in stop_words_list:
            if value < totalDoc:
                terms.append(term)
                value = value + 1
        k += 1
    return terms


def corpus_generation(directory):
    for file in directory:
        folder = open(path + file, "r")
        all_content = ''.join(folder.readlines())
        final_corpus[file] = all_content.split()


def BM25_calculation(n, f, qf, N, dl, avdl, r, R):
    K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
    term1 = math.log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    term2 = (((k1 + 1) * f) / (K + f)) * (((k2 + 1) * qf) / (k2 + qf))
    return term1 * term2


def query_frequency(word, query_text):
    query_freq = 1
    j = 0
    while j < len(query_text):
        if query_text[j] == word:
            query_freq += 1
        j += 1
    return query_freq


def calc_doc_score(query_text, total_content, query_id):
    avdl = calc_avg_length(total_content)
    N = len(total_content)
    queryIDStr = str(query_id)
    if queryIDStr in relevant_list:
        rel = relevant_list[queryIDStr]
        R = len(rel)
    else:
        R = 0
    query_result = BM25_score(query_text, total_content, query_id, avdl, N, R)

    return query_result


def BM25_score(query_text, total_content, query_id, avdl, N, R):
    res = {}
    for each_entry in query_text:
        r = check_present(each_entry, query_id)
        each_entry = each_entry.lower()
        if each_entry in unigram_index:
            query_freq = query_frequency(each_entry, query_text)
            for document_id, frequency in unigram_index[each_entry].items():
                length = len(unigram_index[each_entry])
                score = BM25_calculation(length, frequency, query_freq, N, total_content[document_id], avdl, r, R)
                if document_id not in res:
                    res[document_id] = score
                else:
                    res[document_id] = res[document_id] + score
    return res


def calc_avg_length(all_content):
    document_len = 0.0
    for each_entry in all_content:
        document_len += all_content[each_entry]
    avg = float(document_len) / float(len(all_content))
    return avg


def get_topmost_documents(query_text, query_id):
    all_content = {}
    for each_entry in final_corpus:
        entries = final_corpus[each_entry]
        for each_term in entries:
            if each_term in unigram_index:
                entry = unigram_index[each_term]
                if each_entry not in entry:
                    entry[each_entry] = 1
                else:
                    entry[each_entry] = entry[each_entry] + 1
            else:
                value = {}
                value[each_entry] = 1
                unigram_index[each_term] = value
        each_entry_str = str(each_entry)
        each_corpus = final_corpus[each_entry_str]
        all_content[each_entry] = len(each_corpus)
    query_id = str(query_id)
    top_doc = calc_doc_score(query_text.split(), all_content, query_id)
    return top_doc


def get_all_queries(file):
    updated_query = {}
    index = 0
    folder = open(file)

    all_content = folder.read().split("</DOC>")
    for each_entry in all_content:
        if "<DOC>" in each_entry:
            entry = each_entry.find("<DOC>") + len("<DOC>")
            all_content[index] = each_entry[entry:]
        index += 1
    for each_entry in all_content:
        first = "<DOCNO> "
        last = " </DOCNO>"
        try:
            start = each_entry.index(first) + len(first)
            end = each_entry.index(last, start)
            value = each_entry[start:end]
        except ValueError:
            value = ""
        reg_exp = re.sub(r'<DOCNO>.*</DOCNO>', "", each_entry)
        newLine = "\n"
        updated_query[value] = reg_exp.replace(newLine, " ")
    return updated_query


if __name__ == '__main__':
    query_list = get_all_queries("C:/Users/Ravi/Documents/test-collection/cacm.query")
    get_stop_list()
    corpus_generation(os.listdir(path))
    folder = open("C:/Users/Ravi/Desktop/IR_ProjectRes/BM25_PseudoRel.txt", 'w')
    start = 1
    end = len(query_list)
    for query_id in range(start, end):
        query_string = ""
        string_query = str(query_id)
        final_query = str(query_list[string_query])
        for each_entry in final_query.split():
            query_string = query_string + " " + str(each_entry)
        document_list = get_topmost_documents(query_string, string_query)

        res_document_list = sorted(document_list, key=document_list.get, reverse=True)[:50]

        updatedQuery = query_expansion_technique(res_document_list, query_string)
        queryNew = ""
        for each_entry in updatedQuery:
            string_each_entry = str(each_entry)
            queryNew = queryNew + " " + string_each_entry

        final_result = get_topmost_documents(queryNew + " " + query_string, str(query_id))
        counter = 0

        sortedList = sorted(final_result, key=final_result.get, reverse=True)[:100]
        for each_entry in sortedList:
            counter = counter + 1
            DocID = str(each_entry)
            Score = str(final_result[each_entry])
            folder.write(str(query_id) + " Q0 " + str(DocID)[:-4] + " " + str(counter) + " " \
                         + str(Score) + " PseudoRel-BM25" + "\n")
    folder.close()