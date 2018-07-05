import os
import collections
import preprocess

# load the vocabulary in list form
def get_voca_list(path):
    file = open(path, 'r')
    voca = file.read()
    file.close()
    voca = voca.split(' ')
    return voca

# save the updated vocabulary in a file
def update_voca(voca, file_name):
    file = open(file_name, 'a')
    for word in voca:
        file.write(word + ' ')

if __name__ == "__main__":
    file_name = "vocabulary"
    new_file_name = "newvocabulary"
    voca = get_voca_list(file_name)
    file = open(new_file_name, 'w')
    file.close()
    # save the number of occurrence of every word in all emails
    frequency = collections.defaultdict(lambda : 0)

    path = "users/"
    folder_list = os.listdir(path)

    # count the occurrence of every word in every email
    for folder in folder_list:
        if folder[0] == '.':
            continue
        else:
            destpath = path + folder + "/all_documents"
            print "ready to process " + folder
            if os.path.exists(destpath):
                emails = preprocess.process_folder(destpath)
                print "email list for " + folder + " has been established" + " number is: " + str(len(emails))
                for email in emails:
                    for word in email.content:
                        frequency[word] += 1

    for word in frequency:
        # the value after "<" can be tuned
        if frequency[word] < 100:
            if word in voca:
                voca.remove(word)
            else:
                continue

    print len(voca)
    update_voca(voca, new_file_name)
