
Extra Credit:
--------------
Download the ExtraCredit directory.

************************************************************************************************************************************************************

1. ExactMatch - Execute the "python3 ExactMatch.py" and the result file called "Relevant_doc_exactmatch.txt" will generated inside the ExtraCredit directory.

Dependencies:
--------------
import glob
import operator
import os
import re
import shutil
from collections import Counter
from math import log

Parameters for the script:
--------------------------
Open the script and set the below mentioned parameters for the following variables inside the script wherever applicable:

1. docCollectionPath = > The location of the cleaned corpus where all the document terms are in lowercase 
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"

2. rel_file => The location of the cacm.rel file or any other relevance file you want to use . Used in BM25 calculation for final ranking
e:g => rel_file = open ('/Users/dipanjan/gitHub/Python-Projects/FinalProject/test-collection/cacm.rel.txt', 'r')

3. queryFile = Location of a clean query file
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/query2.txt"


Example of a clean query file:
------------------------------
carbon footprint
carbon
carbon footprint greenhouse

************************************************************************************************************************************************************

2. BestMatch - Execute the "python3 BestMatch.py" and the result file called "Relevant_doc_bestmatch.txt" will generated inside the ExtraCredit directory.

Dependencies:
--------------
import glob
import operator
import os
import re
import shutil
from collections import Counter
from math import log

Parameters for the script:
--------------------------
Open the script and set the below mentioned parameters for the following variables inside the script wherever applicable:

1. docCollectionPath = > The location of the cleaned corpus where all the document terms are in lowercase 
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"

2. rel_file => The location of the cacm.rel file or any other relevance file you want to use . Used in BM25 calculation for final ranking
e:g => rel_file = open ('/Users/dipanjan/gitHub/Python-Projects/FinalProject/test-collection/cacm.rel.txt', 'r')

3. queryFile = Location of a clean query file
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/query2.txt"


Example of a clean query file:
------------------------------
carbon footprint
carbon
carbon footprint greenhouse

************************************************************************************************************************************************************

3. Ordered BestMatch with proximity N  - Execute the "python3 BestMatch_Proximity.py" and the result file called "Relevant_doc_bestMatch_proximity.txt" will generated inside the ExtraCredit directory.

Dependencies:
--------------
import glob
import operator
import os
import re
import shutil
from collections import Counter
from math import log

Parameters for the script:
--------------------------
Open the script and set the below mentioned parameters for the following variables inside the script wherever applicable:

1. docCollectionPath = > The location of the cleaned corpus where all the document terms are in lowercase 
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"

2. rel_file => The location of the cacm.rel file or any other relevance file you want to use . Used in BM25 calculation for final ranking
e:g => rel_file = open ('/Users/dipanjan/gitHub/Python-Projects/FinalProject/test-collection/cacm.rel.txt', 'r')

3. queryFile = Location of a clean query file
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/query2.txt"

4. slider = the value of N (proximity)

Example of a clean query file:
------------------------------
carbon footprint
carbon
carbon footprint greenhouse

************************************************************************************************************************************************************
4. Ordered ExactMatch with Proximity N - Execute the "python3 ExactMatch_Proximity.py" and the result file called "Relevant_doc_exactmatch_proximity.txt" will generated inside the ExtraCredit directory.

Dependencies:
--------------
import glob
import operator
import os
import re
import shutil
from collections import Counter
from math import log

Parameters for the script:
--------------------------
Open the script and set the below mentioned parameters for the following variables inside the script wherever applicable:

1. docCollectionPath = > The location of the cleaned corpus where all the document terms are in lowercase 
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/raw-documents1/"

2. rel_file => The location of the cacm.rel file or any other relevance file you want to use . Used in BM25 calculation for final ranking
e:g => rel_file = open ('/Users/dipanjan/gitHub/Python-Projects/FinalProject/test-collection/cacm.rel.txt', 'r')

3. queryFile = Location of a clean query file
e:g => "/Users/dipanjan/gitHub/GroupProject/FinalProject/ExtraCredit/test-data/query2.txt"

4. slider = the value of N (proximity)

Example of a clean query file:
------------------------------
carbon footprint
carbon
carbon footprint greenhouse

************************************************************************************************************************************************************
