Phase 2 - Snippet Generation:
------------------------------
Navigate inside the SnippetGeneration directory
Execute  " python3 snippet.py" to generate snippets. 

Dependencies:
--------------
import os
import re
import shutil
import dominate
from bs4 import BeautifulSoup
from dominate.tags import *

Parameters for the script:
---------------------------
Open the script snippet.py and set the below mentioned parameter avaiable at the top of the script below the import section

SNIPPET => Location whether the snippet files will be generated (e:g : 'snippets/')
RAW_HTML_PATH = > Location of cacm raw html files (e:g : '/Users/dipanjan/gitHub/GroupProject/FinalProject/test-collection/cacm/')
BM25_RES => Location of BM25 output result file containing the ranking for all 64 queries ( e:g :'/Users/dipanjan/gitHub/GroupProject/FinalProject/BM25_Results/BM25.txt')
QUERY_PATH = Location of cacm.query.txt ( e:g : '/Users/dipanjan/gitHub/GroupProject/FinalProject/test-collection/cacm.query.txt')
COMMON_WORD= Location of common_words  ( e:g :'/Users/dipanjan/gitHub/GroupProject/FinalProject/test-collection/common_words')
WINDOW = The number of terms to be present in the snippet ( e:g : 40)

============================================================================================================================================================
