import nltk.data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
import types
import pandas as pd
import csv
import glob,os,re,sys
from pathlib import Path
#from google.colab import drive
from collections import defaultdict

import multiprocessing as mp
import time

import MyFun,variables
print(os.getcwd())

#all_files=[]
csv_filename_pattern = r'([a-zA-Z]{1,6}_\d{1,2}_\d{4}_\d{2}_\d{2})'

def initialize():

    output_directory = Path(os.getcwd()+"/output/")
    if( output_directory.exists() and output_directory.is_dir()) :
    #print(os.getcwd()+"/output/")
        print(output_directory.as_uri())
        print("directory already exists")

    else:  
        os.mkdir(os.getcwd()+"/output/")
        print(os.getcwd()+"/output/")
        print("directory is created")


    existing_files = sorted(Path(os.getcwd()+"/output/").iterdir(), key=os.path.getmtime)

    all_files = glob.glob("./input/*.txt")

    print(len(all_files))


    existing_file_counts = defaultdict(int)



    file_counter = 0
    for file in existing_files:
        if(file.stat().st_size==0):
            print(f"{file.name} is removed")
            file.unlink()
            continue
        name = re.search(csv_filename_pattern,file.name,re.IGNORECASE).group(1)
        existing_file_counts[name]+=1
        #print(f"{file_counter} : {name}")
        file_counter+=1



    all_files_count = len(all_files)
    for key,value in existing_file_counts.items():
    #print(key,value)
        if(value == 2):
            all_files.remove(key+".txt")


    print(f"{all_files_count-len(all_files)} files already processed. {len(all_files)} will be processed only. ")

    #rid = 0
    #sentences = {}
    #filenames=[]

    return all_files

causal_verbs = variables.causal_verbs
reverse_causal_verbs = variables.reverse_causal_verbs

def tokenize_sentences(idx,file_name):
    #print(f"beginning {idx,file_name}")
    #read all txt file 
    text = Path(file_name).read_text('utf-8')
    #filenames.append(os.path.basename(text_path))
    
    
    #create a dictionary and assign each sentence to a dictionary.
    #dictionary will hold the sentences of each file
    #sentences[idx] = []
    text = text.strip()
    #extract each sentence and assign to corresponding the dictionary
    
    text = text.replace("▪"," .")
    text = text.replace("•"," .")  
    text = text.replace("·"," .")
    
    text = text.replace(".",". ")
 
    #return (idx)
    sentences = sent_detector.tokenize(text)

    name = re.search(csv_filename_pattern,file_name,re.IGNORECASE).group(1)

    missed_verbs_new = name+"_"+variables.missed_verbs
    Cause_Effect_Pairs_new = name+"_"+variables.Cause_Effect_Pairs
    #print("")
    #print(missed_verbs_new)
    #print(Cause_Effect_Pairs_new)
    #print("")




    
    
    missed_verbs_csv = open(os.getcwd()+"/output/"+missed_verbs_new,"w") #<===open and write to a csv file  and New file is created.
    missed_verbs_writer = csv.writer(missed_verbs_csv, quoting = csv.QUOTE_NONNUMERIC)
    missed_verbs_writer.writerow(["verb","sentence"])
    missed_verbs_csv.close()
    

    csvOutput = open(os.getcwd()+"/output/"+Cause_Effect_Pairs_new,"w")    
    csvWriter = csv.writer(csvOutput, quoting = csv.QUOTE_NONNUMERIC)
    csvWriter.writerow(["file name","direction","verb","cause","effect","sent"])


    
    for sent in sentences:
        #parts = get_verb_left_right(sent)
        #print("#####")
        #print(sent)
        try:
          part_list = MyFun.get_verb_left_right(sent,missed_verbs_new)
        except:
          print(f"Error {sys.exc_info()[0]}  = {sent}")
        
        if(part_list):
          for parts in part_list:
            if parts:
                verb = parts[0]
                if verb.lower() in causal_verbs:
                    #count += 1
                    cause = parts[1]
                    effect = parts[2]
                    #print("Found causal verb and cause-effect pairs: ([{}],[{}],[{}]) from sentence: {}".format(verb,cause,effect,sent))
                    csvWriter.writerow([file_name,"forward",verb,cause,effect,sent])
                    print("f", end='')
                elif verb.lower() in reverse_causal_verbs:
                    #count += 1
                    cause = parts[2]
                    effect = parts[1]
                    csvWriter.writerow([file_name,"reverse",verb,cause,effect,sent])
                    print("b", end='')
                    #print("Found reverse causal verb and cause-effect pair: ([{}],[{}],[{}]) from sentence: {}".format(verb,cause,effect,sent))        
                    #print("Found {} cause-effect pairs.".format(count))
                
                #write to file after every 50 sentence


        #csvOutput.close()
    
    csvOutput.close()


if __name__ == '__main__':    

    all_files = initialize()
    p=mp.Pool(1)

    print(f"total number of files {len(all_files)}")
    beg = time.time()

    #print(all_files[:10])
    results = p.starmap(tokenize_sentences,enumerate(all_files))

    print(f"time diff = {time.time()-beg}")