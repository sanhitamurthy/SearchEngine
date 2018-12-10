Phase 3 : Evaluation

FOLDER STRUCTURE:
1. Source Code is evaluation.py
2. Input files are in Input directory
3. Output files are generated in Output directory
4. The results for all our runs are zipped as Results.zip

--------------------------------------
Results folder:

The subfolders containing the results are labelled with the correspinding names of the baseline runs. For example, The results of BM25 with no stopping are in the folder "BM25_NO_STOPPING"

Each subfolder contains results for P@5, P@20 and Precision/Recall values for all the queries.
Values of MAP and MRR are stored in MAP.txt and MRR.txt

precision_recall_curve_plot.png is the interpolated recall precision plot.

----------------------------------------

To run :
Follow instructions to install matplotlib here https://matplotlib.org/users/installing.html
Run 'python evaluation.py'

----------------------------------------
FILE FORMATS:


File Format for Precision Recall Values File:
QueryID Q0 DOCID RANK SCORE X PRECISION RECALL

Where X is R if its a relevant document and N if its not relevant

----------------------------------------
File format for P@5 and P@20 files:

QUERYID  PRECISION "P@K"

Where PRECISION is the value of P@K
k=5 or 20

-----------------------------------------
MAP and MRR:

MAP values for each run is present on a separated line along with the name of the run (BM25,TFIDF,lucene,QL)
The suffix of Task3a are the runs with stopping
BM25_PR is the BM25 run with pseudorelevance








