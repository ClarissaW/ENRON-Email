import preprocess
import os

# from pyspark.mllib.clustering import LDA, LDAModel
# from pyspark.mllib.linalg import Vectors
# $ PYSPARK_PYTHON=python3.4 bin/pyspark
# $ PYSPARK_PYTHON=/opt/pypy-2.5/bin/pypy bin/spark-submit examples/src/main/python/pi.py

######### attention ##########
#    absolute path in MAC    #
##############################
path = "users/"
folder_list = os.listdir(path)
# save the vocabulary
biggest_vocabulary = set()
filevocabulary = "vocabulary"
file_vocabulary = open(filevocabulary, 'w')
file_vocabulary.close()
#
filelogs = "logs"
file_log = open(filelogs, 'w')
file_log.close()
# the number of all emails
total_emails = 0
################################################################################
print "start to process folders"
file_log = open(filelogs, 'a')
# for every folder
for folder in folder_list:
    file_log.write(folder + "\n")
    if folder[0] == '.': # if the folder is not a hidden folder
        continue
    else:
        destpath = path + folder + "/all_documents"
        print "ready to process " + folder
        if os.path.exists(destpath):# in case of some folders don't have "all_documents"
            # emails is the info of all email in this folder
            emails = preprocess.process_folder(destpath)
            print "email list for " + folder + " has been established" + " number is: " + str(len(emails))
            total_emails += len(emails)
            #
            biggest_vocabulary.update(preprocess.vocabulary)
            print "vocabulary for " + folder + " has been established"

file_log.close()
###############################################################################
# transform to list type for convenient operating
biggest_vocabulary = list(biggest_vocabulary)
# save vocabulary to file
file_vocabulary = open(filevocabulary, 'a')
for word in biggest_vocabulary:
    file_vocabulary.write(word + " ")
file_vocabulary.close()
print "vocabulary is written"
print "number of total emails " + str(total_emails)
