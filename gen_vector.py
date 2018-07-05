import os
import preprocess
import statistics
import math

path = "users/"
folder_list = os.listdir(path)

file_id = open("email_ID", 'w')
file_id.close()

path_vector = "vectors"
file_vector = open(path_vector + "/kmeans", 'w')
file_vector.close()

file_libsvm = open(path_vector + "/svm", 'w')
file_libsvm.close()
#################################################################
# For each folder, build the vector and write

################ import the vocabulary ##########################
file_vocabulary = open("newvocabulary", 'r')
vocabulary = file_vocabulary.read()
vocabulary = vocabulary.split(' ')
file_vocabulary.close()
size_vocabulary = len(vocabulary)
email_counter = 0 # i.e. email ID

#################################################################
for folder in folder_list:
    if folder[0] == '.':
       continue
    else:
        print "ready to process " + folder
        destpath = path + folder + "/all_documents"
        if os.path.exists(destpath):
            emails = preprocess.process_folder(destpath)
            users = statistics.stat(emails)
        else:
            continue
# statistic
    DF = [0] * size_vocabulary
    IDF = [0] * size_vocabulary
    # compute the DF
    for email in emails:
        email.vector = [0] * size_vocabulary
        flag = [0]*size_vocabulary
        for word in email.content:
            if word in vocabulary:
                index = vocabulary.index(word)
                email.vector[index] += 1
                if flag[index] == 0:
                    DF[index] += 1
                    flag[index] = 1
                else:
                    continue
    # compute the IDF
    for i in range(0, size_vocabulary):
        IDF[i] = math.log((size_vocabulary + 1)/(DF[i] + 1), 2)

    print "feature for " + folder + " has been calculated"
# write to the file
    file_vector = open(path_vector + "/kmeans", 'a')
    file_libsvm = open(path_vector + "/svm", 'a')
    file_id = open("email_ID", 'a')
    for email in emails:
        email_counter += 1
        file_libsvm.write(str(email_counter) + " ")
        file_id.write(str(email_counter) + "\t" + str(email.filepath) + "\n")
        for i in range(0, size_vocabulary):
            # compute the TFIDF
            weight = email.vector[i]
            weight *= IDF[i]
            weight = round(weight, 1)
            email.vector[i] = weight
            #
            if i == size_vocabulary - 1: # if is the last weight
                file_vector.write(str(weight) + "\n")
                file_libsvm.write(str(i + 1) + ":" + str(weight) + "\n")
            else:
                file_vector.write(str(weight) + " ")
                file_libsvm.write(str(i + 1) + ":" + str(weight) + " ")

    file_vector.close()
    file_id.close()
    file_libsvm.close()

    print "vectors for " + folder + " has been recorded"
