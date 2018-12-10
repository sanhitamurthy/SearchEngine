import pdb
stemmed_file_path = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/test-collection/test-collection/cacm_stem.txt"
stemmed_output_path = "C:/Users/kmcar/OneDrive/Documents/IR/FinalProject/Phase1/Task3/stemmed_files/"

def create_stemmed_files():
    docID = None
    file_contents = ""
    output_file = ""
    with open(stemmed_file_path,'r') as file:
        for line in file:
            if line[0] == '#':
            #write previous file contents
                determine_fileName(docID,file_contents)
                docID = line[2:len(line)-1]
                file_contents = ""
                continue;
            else :
                file_contents+=line
    determine_fileName(docID,file_contents)

def determine_fileName(docID,file_contents):
    if docID == None :
        pass
    elif len(docID) == 1:
        output_file = "CACM-000"+docID
        write_file_contents(output_file,file_contents)
    elif len(docID) == 2 :
        output_file = "CACM-00"+docID
        write_file_contents(output_file,file_contents)
    elif len(docID) == 3 :
        output_file = "CACM-0"+docID
        write_file_contents(output_file,file_contents)
    elif len(docID) == 4 :
        output_file = "CACM-"+docID
        write_file_contents(output_file,file_contents)


def write_file_contents(output_file,file_contents):
    # pdb.set_trace()
    with open(stemmed_output_path+output_file+".txt",'w') as output:
        output.write(' '.join(file_contents.split()))
def main():
    print ("Creating stemmed files")
    create_stemmed_files()

if __name__ == '__main__':
    main()
