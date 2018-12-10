# Evaluation of the effectiveness of the retreival system runs
# Measures of effectiveness implemented:
# 1. Mean Average Precision
# 2. Mean Reciprocal Rank
# 3. P@K , K=5 and K=20
# 4. Precision and Recall with plot

import os
import pdb
import matplotlib.pyplot as plt

RELEVANCE_JUDGEMENTS = "cacm.rel.txt"
#4 BASELINE RUNS
BM25_RUN = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/BM25_Task1.txt"
TFIDF_RUN = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/TFIDF_Task1.txt"
QL_RUN = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/QL_Task1.txt"
LUCENE = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/lucene.txt"

#Query enrichment RUN
PSEUDORELEVANCE = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/BM25_PR.txt"

#3 stopping runs: BM25,Tfidf,QL
BM25_STOPPING = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/BM25_Task3a.txt"
TFIDF_STOPPING ="C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/TFIDF_Task3a.txt"
QL_STOPPING = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase3/output/QL_Task3a.txt"

MAP_EVALUATION_SCORE = "MAP_EVALUATION_SCORE.txt"
MRR_EVALUATION_SCORE = "MRR_EVALUATION_SCORE.txt"

relevantDict = {}
interpolated_PRValues={}

def createDict(FILENAME):
    ranking = {}
    with open(FILENAME,"r") as file:
        for line in file:
            # pdb.set_trace()
            queryID = line.split()[0]
            if queryID not in ranking.keys():

                ranking[queryID] = [' '.join(line[:-1].split()[2:])]
                # pdb.set_trace()
            else:
                ranking[queryID].append(' '.join(line[:-1].split()[2:]))
    return ranking




def evaluate_PK(FILENAME, retreivedDict):
    p5 = {}
    p20 = {}
    queryID = 1
    file = FILENAME[:FILENAME.rindex('.')]
    pk5_output_file = open(file+"_P5_EVALUATION.txt",'w')
    pk20_output_file = open(file+"_P20_EVALUATION.txt",'w')
    numQueries =  len(relevantDict.keys())
    # pdb.set_trace()
    while queryID <= numQueries:
        if not relevantDict.get(str(queryID)):
            p5[queryID] = 0.0
            p20[queryID] = 0.0
            queryID+=1
            continue

        relevantDocs = relevantDict[str(queryID)]
        # pdb.set_trace()
        top5Docs = retreivedDict[str(queryID)][:5]
        top20Docs = retreivedDict[str(queryID)][:20]

        p5[queryID] = calculatePK(5,top5Docs,relevantDocs)
        pk5_output_file.write(str(queryID)+ " " + str(p5[queryID]) +" P@5 \n")
        p20[queryID] = calculatePK(20,top20Docs,relevantDocs)
        pk20_output_file.write(str(queryID)+ " " + str(p20[queryID]) +" P@20 \n")
        queryID+=1
    pk5_output_file.close()
    pk20_output_file.close()

def calculatePK(k,topKDocs,relevantDocs):

    relevant_Doc_counter = 0
    for doc in topKDocs:
        docID = doc.split()[0]
        for relevant_doc in relevantDocs:
            if docID == relevant_doc.split()[0]:
                relevant_Doc_counter +=1
    return relevant_Doc_counter/k

def evaluate_precision_recall(FILENAME, retreivedDict ):
    QUERIES_LEN = len(relevantDict)
    precisionValues = {}
    recallValues = {}
    totalAvgPrecision = 0
    output_file = open(FILENAME[:len(FILENAME)-4]+"_PRECISION_RECALL_EVAL","w")

    for queryID in retreivedDict:
        sumPrecisionValues = 0
        avgPrecision = 0
        numRetrievedDocs = 0
        currentCount_rel_and_retreived = 0
        precisionValues[queryID] = []
        recallValues[queryID] = []

        if queryID in relevantDict.keys():
            relevantDocs = relevantDict[queryID]
            for ret_doc in retreivedDict[queryID] :
                numRetrievedDocs +=1
                rel_and_retreived = False
                ret_docID,ret_docRank,ret_docScore =  ret_doc.split()[0],ret_doc.split()[1],ret_doc.split()[2]
                for relevant_doc in relevantDocs :
                    rel_docID = relevant_doc.split()[0]
                    if ret_docID == rel_docID:
                        rel_and_retreived = True
                        break;
                if rel_and_retreived :
                    currentCount_rel_and_retreived+=1
                doc_precision = round(float(currentCount_rel_and_retreived)/float(numRetrievedDocs),4)
                precisionValues[queryID].append({ret_docID : doc_precision})
                doc_recall = round(float(currentCount_rel_and_retreived)/float(len(relevantDocs)),4)
                recallValues[queryID].append({ret_docID: doc_recall})
                if rel_and_retreived :
                    sumPrecisionValues = sumPrecisionValues + doc_precision
                    output_file.write(str(queryID)+" Q0 "+ret_docID+" "+ str(ret_docRank) + " "+str(ret_docScore) + " R " + str(doc_precision)
                        +" "+str(doc_recall)+"\n" )
                else:
                    output_file.write(str(queryID)+" Q0 "+ret_docID+" "+ str(ret_docRank) + " "+str(ret_docScore) + " N " + str(doc_precision)
                        +" "+str(doc_recall)+"\n" )

            if currentCount_rel_and_retreived != 0:
                avgPrecision = round(avgPrecision + float(sumPrecisionValues)/float(currentCount_rel_and_retreived),4)
            else:
                avgPrecision = 0
            totalAvgPrecision = totalAvgPrecision + avgPrecision
        else:
            continue
    calculateMAP(FILENAME, totalAvgPrecision, QUERIES_LEN)
    processPRValues(precisionValues[str(10)][:100],recallValues[str(10)][:100],FILENAME)
    output_file.close()

#Precision and Recall Values for queryID=1
def plotPrecisionRecallCurve(precisionValues, recallValues,FILENAME) :

    interpolatedList = interpolate(precisionValues,recallValues)
    int_precisionValues = []
    int_recallValues = []
    for list in interpolatedList :
        recall = list[0]
        precision = list[1]
        int_recallValues.append(recall)
        int_precisionValues.append(precision)
    plot(int_recallValues,int_precisionValues,FILENAME)

def consolidateRecallValues(recallValues,precisionValues,FILENAME):
    for i in range(0,len(recallValues)):
        recall = recallValues[i]
        precision = precisionValues[i]
        if recall not in interpolated_PRValues:
            interpolated_PRValues[recall] = [precision]
        else :
            precisionList = interpolated_PRValues[recall]
            if precision not in precisionList :
                interpolated_PRValues[recall].append(precision)


def processPRValues(precisionDict, recallDict,FILENAME):
        precisionValues = extractPRValues(precisionDict)
        recallValues = extractPRValues(recallDict)
        plotPrecisionRecallCurve(precisionValues, recallValues,FILENAME)

def plot(x,y,FILENAME):
        axis= [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        plt.xticks(axis)
        plt.yticks(axis)
        COLOR = setPlotColors(FILENAME)
        plt.plot(x,y,color=COLOR)
        plt.savefig("plot.png")

def setPlotColors(FILENAME):
    COLOR =''
    if FILENAME == BM25_RUN :
        COLOR = 'red'
    elif FILENAME == TFIDF_RUN :
        COLOR = 'green'
    elif FILENAME == QL_RUN :
        COLOR = 'blue'
    elif FILENAME == LUCENE :
        COLOR = 'black'
    elif FILENAME == PSEUDORELEVANCE :
        COLOR = 'orange'
    elif FILENAME == BM25_STOPPING :
        COLOR = 'purple'
    elif FILENAME == TFIDF_STOPPING :
        COLOR = 'olive'
    elif FILENAME == QL_STOPPING :
        COLOR = 'cyan'
    return COLOR

def extractPRValues(dict):
    values=[]
    for val in dict :
        for key in val.keys():
            values.append(val[key])
    return values

def interpolate(precisionValues,recallValues) :
    pr_dict = unintrapolate(precisionValues,recallValues)
    interpolated_values = []
    for val in range(0,len(recallValues)):
        recall = recallValues[val]
        max_precision = pr_dict[recall]
        for p in range(val, len(recallValues)):
            curr = precisionValues[p]
            max_precision = max(max_precision,curr)

        interpolated_values.append([recall,max_precision])
    return interpolated_values

def unintrapolate(precisionValues,recallValues):
    pr_dict = {}
    for val in range(0,len(recallValues)):
        recall = recallValues[val]
        current_precision = precisionValues[val]
        if recall not in pr_dict.keys():
            pr_dict[recall] = current_precision
        else:
            max_precision = pr_dict[recall]
            if current_precision > max_precision :
                 pr_dict[recall] = current_precision
    return pr_dict

def calculateMAP(FILENAME,avgPrecision,numberOfQueries):
    mean_avg_precision = round(float(avgPrecision)/float(numberOfQueries),4)
    with open(MAP_EVALUATION_SCORE,'a') as file :
        file.write("Mean Avg Precision of " +str(FILENAME[:len(FILENAME)-4])+" is "+ str(mean_avg_precision)+ "\n")


def evaluateMRR(FILENAME,retreivedDict):
    sum_reciprocal_rank = 0
    numQueries =  len(relevantDict.keys())
    for queryID in range(1,numQueries+1) :
        if str(queryID) in relevantDict.keys():
            relevantDocs = relevantDict[str(queryID)]
            retrievedDocs = retreivedDict[str(queryID)]
            for retrievedDoc in retrievedDocs:
                retrieved_and_relevant = False
                ret_docID = retrievedDoc.split()[0]
                for relevantDoc in relevantDocs:
                    rel_docID =  relevantDoc.split()[0]
                    if ret_docID == rel_docID:
                        retrieved_and_relevant = True
                        reciprocal_rank = 1.0/ float(retrievedDoc.split()[1])
                        sum_reciprocal_rank += reciprocal_rank
                        break
                if retrieved_and_relevant :
                    break

    mean_reciprocal_rank = round(sum_reciprocal_rank/ float(numQueries),4)
    with open (MRR_EVALUATION_SCORE,'a') as f :
        f.write("Mean Reciprocal Rank for "+str(FILENAME[:-4]) + " is " + str(mean_reciprocal_rank) + "\n")


def evaluateBaselineRuns(FILENAME):
    retrievedDict = createDict(FILENAME)
    evaluate_precision_recall(FILENAME,retrievedDict)
    evaluate_PK(FILENAME,retrievedDict)
    evaluateMRR(FILENAME,retrievedDict)

def main():
    global relevantDict
    relevantDict = createDict(RELEVANCE_JUDGEMENTS)
    evaluateBaselineRuns(TFIDF_RUN)
    evaluateBaselineRuns(BM25_RUN)
    evaluateBaselineRuns(QL_RUN)
    evaluateBaselineRuns(LUCENE)
    evaluateBaselineRuns(PSEUDORELEVANCE)
    evaluateBaselineRuns(TFIDF_STOPPING)
    evaluateBaselineRuns(BM25_STOPPING)
    evaluateBaselineRuns(QL_STOPPING)



def find_avgPrecision_atStdRecallLevels(FILENAME):
    R = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    y=[]
    val={}

    for i in range(0, len(R)):
        recall = R[i]
        if recall in interpolated_PRValues.keys():
            precisionValues = interpolated_PRValues[recall]
            sum=0
            for p in precisionValues:
                sum+=p
            print(len(precisionValues))
            avg = sum/len(precisionValues)

            val[recall] =avg
    for i in range(0, len(R)):
        y.append(val[R[i]])
        print(str(R[i])+" "+str(val[R[i]]))

    plot(R,y,FILENAME)




if __name__ == "__main__" :
    main()
