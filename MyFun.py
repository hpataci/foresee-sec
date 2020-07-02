import os,csv,re
import variables

from allennlp.predictors.predictor import Predictor



predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz")



patternVerb = r'\[V: (.*?)\]'
patternLeft = r'\[ARG0: (.*?)\]'
patternRight= r'\[ARG1: (.*?)\]'




def get_unique_fileName(fileName,inputPath=""):
  print("")
  file_name = fileName
  if os.path.isfile(inputPath+file_name):
    expand = 1


    while True:
        expand += 1
        splits = os.path.splitext(file_name)
        new_file_name = splits[0] + "__"+str(expand) + splits[1]
        if os.path.isfile(inputPath+new_file_name):
            continue
        else:
            file_name = new_file_name
            break
  
  #print("generated: fileName {0}".format(file_name))
  return file_name




def get_verb_left_right(sentence):
    
    #global missed_verbs_new
    #global all_verbs
    verb = None
    left_np = None
    right_np = None
    #print("############################################################### input sentence: {0}".format(sentence))
    #print(missed_verbs)

    missed_verbs_csv = open(os.getcwd()+"/output/"+variables.missed_verbs_new,"a") # <===open and write to a csv file  and New rows will be appended.
    missed_verbs_writer = csv.writer(missed_verbs_csv, quoting = csv.QUOTE_NONNUMERIC)

    # if sentence doesn't contain the causal verbs, return
    if not any((word in sentence) for word in variables.all_causal_verbs)  :
      missed_verbs_writer.writerow(["NONE",sentence])
      missed_verbs_csv.close()
      print(".", end='')
      return

    #parse the sentence
    result = predictor.predict(
      sentence=sentence
    )

    #list for parse trees that contain the causal verbs and arguments
    verb_arguments_list =[]

    for elem in result['verbs']:
      failed = True
      #extract verb from the parse tree
      #m = re.search(patternVerb, elem['description'], re.IGNORECASE)
      #print("foo : {0} ".format(elem['verb']))
      verb = elem['verb']

      if(len(verb)>0):
        
        #if verb is a causal verb, continue
        if(verb in variables.all_causal_verbs):
          
          #extract left argument from the sentence
          m = re.search(patternLeft, elem['description'], re.IGNORECASE)
          if(m):
            left_np = m.group(1)

            #extract right argument from the sentence
            m = re.search(patternRight, elem['description'], re.IGNORECASE)
            if(m):
              failed = False
              right_np = m.group(1)
              
              # when verb, left argument, right argument are all extracted, add them to the list
              verb_arguments_list.append((verb,left_np,right_np))
              #print("######pushed {0}".format((verb,left_np,right_np)))
        
        if(failed):
          #print("!! '{0}' not found in the causal verbs list ".format(verb))
          #write the discarded verb to the file
          missed_verbs_writer.writerow([verb,sentence])

    missed_verbs_csv.close()

    return verb_arguments_list