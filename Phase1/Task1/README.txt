Task1:

1. Folder: corpus_clean-->
*corpus_clean.py takes the cacm corpus as the source and produces a clean corpus in the given destination. 
*Change the path of the 'source' folder to the location where the cacm corpus is present.
*Change the path of the 'clean_corpus_dest' folder to the location where the clean corpus needs to be stored.
*Run the main function by right clicking inside the file corpus_clean.py  and clicking on ‘Run’

2. Folder: cleaning_cacm.query-->

*cleaning_cacm_query.py takes the 'cacm.query.txt' as input and produces a result with the cleaned queries
*Change the path of the 'queries_source' folder to the location where the cacm.query.txt is present.
*Change the path of the 'final_query_text' folder to the location where the cleaned queries needs to be stored.
*Run the main function by right clicking inside the file cleaning_cacm_query.py and clicking on ‘Run’

3. Folder: Task1_src -->

BM25.py :

*The program ranks documents based on BM25 algorithm.
*Change the path of the 'clean_corpus' folder to the location where the clean corpus is present.
*Change the path of the 'final_query_text' folder to the location where the cleaned queries is present
*Change the path of the 'cacm_rel_path' folder to the location where the 'cacm.rel.txt' is present.
*Change the path of the 'top_bm25_files' folder to the location to store the result of the top BM25 documents
Run the main function by right clicking inside the file BM25.py and clicking on ‘Run’

QUERY_LIKELIHOOD.py :

*The program ranks documents based on Smoothed Query Likelihood model.
*Change the path of the 'clean_corpus' folder to the location where the clean corpus is present.
*Change the path of the 'final_query_text' folder to the location where the cleaned queries is present
*Change the path of the 'top_ql_files' folder to the location to store the result of the top ranked query likelihood documents
*Run the main function by right clicking inside the file QUERY_LIKELIHOOD.py and clicking on ‘Run’


TF_IDF.py:

*The program ranks documents based on TD-IDF algorithm.
*Change the path of the 'clean_corpus' folder to the location where the clean corpus is present.
*Change the path of the 'final_query_text' folder to the location where the cleaned queries is present
*Change the path of the 'top_tfidf_files' folder to the location to store the result of the top ranked tfidf documents
*Run the main function by right clicking inside the file TF_IDF.py and clicking on ‘Run’

4. Folder: Lucene

*The program ranks documents based on the default Lucene.
*Change the path of the 'scan' on line 94 to the location where the cleaned queries is present.
*Change the path of the 'rsultFile' folder to the location to store the result of the top ranked lucence documents
*Run the main function by right clicking inside the file Lucene.java and clicking on ‘Run’

5. Folder:input_files

*This folder contains all the input files to the programs


5. Folder:outputs

*This folder contains the outputs for the 4 baseline runs.





