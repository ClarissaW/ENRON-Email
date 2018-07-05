import  statistics
import preprocess
import os

path = "users/"
folder_list = os.listdir(path)
file = open("vectors/topic_for", 'w')
for folder in folder_list:
    if folder[0] == '.':
        continue
    else:
        destpath = path + folder + "/all_documents"
        if os.path.exists(destpath):
            emails = preprocess.process_folder(destpath)
            users = statistics.stat(emails)
            for user in users:
                info = users[user]
                for contact in info.frequency:
                    line = info.name.strip('\n') + "to " + contact.strip('\n') + " " + info.frequency[contact].strip('\n') + "\n"
                    # print line
                    file.write(line)

file.close()