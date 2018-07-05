import preprocess
from collections import Counter
import collections

class userinfo:
    def __init__(self):
       self.name = ""
       self.connections = list()
       self.contacts = list()
       self.frequency = collections.defaultdict(lambda : [])
       self.avg_content_length = 0
       self.sents = 0
       self.topic = ""

def stat(emails):
    users = {}
    vocabulary = set()

    # load emai_ID
    ids = {}
    file = open("email_ID", 'r')
    lines = file.readlines()
    for line in lines:
        line = line.strip('\n')
        line = line.split('\t')
        ids[line[1]] = line[0]

    # load email_topics
    e_topic = {}
    file = open("vectors/topic_for_mail", 'r')
    lines = file.readlines()
    for line in lines:
        line = line.strip('\n')
        line = line.split(": ")
        e_topic[line[0]] = line[1]

    for email in emails:
        username = email.name
        id = ids[email.filepath]
        if email.name in users:
            users[username].sents += 1
            users[username].avg_content_length += email.content_length
            users[username].connections += email.to
            for contacts in email.to:
                users[username].frequency[contacts].append(e_topic[id])
        else:
            users[username] = userinfo()
            users[username].name = username
            users[username].sents += 1
            users[username].avg_content_length += email.content_length
            users[username].connections += email.to
            for contacts in email.to:
                users[username].frequency[contacts].append(e_topic[id])

    for user in users:
        users[user].avg_content_length /= users[user].sents
        users[user].contacts = set(users[user].connections)
        info = users[user]
        for people in info.frequency:
            topic_count = Counter(info.frequency[people])
            info.frequency[people] = topic_count.most_common()[0][0]
        # print user, ":\n", info.sents, info.avg_content_length, len(info.connections), len(info.contacts)

    # for contacts in info.contacts:
    #     print contacts, info.frequency[contacts]

    return users
