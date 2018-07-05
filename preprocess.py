# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
porter = PorterStemmer()
import string
import os
import re
######################################################################
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
pattern_web = re.compile(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")
pattern_url = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")
vocabulary = set()
#######################################################################

class metadata:
    def __init__(self):
        self.name = ""
        self.date = ""
        self.subject = ""
        self.to = ""
        self.cc = ""
        self.bcc = ""
        self.origin = ""
        self.content = []
        self.vocabulary = set()
        self.vector = []
        self.content_length = 0
        self.total_length = 0
        self.filepath = ""

    def show(self):
        print "name: ", self.name
        print "date: : ", self.date
        print "To: ", self.to
        print "Subject: ", self.subject
        print "cc: ", self.cc
        print "bcc: ", self.bcc
        print "Origin: ", self.origin
        print "total_length: ", self.total_length
#####################################################################

def process_names(names):
    if ", " in names:
        name_list = names.split(", ")
        # print name_list
        return name_list
    else:
        return [names]

def process_content(content):
    # trailing the content
    content = content.split("---")[0]
    content = content.split("*")[0]
    content = pattern_web.sub('', content)
    content = pattern_url.sub('', content)
    # remove punctuations & digits
    content = content.translate(None, string.punctuation)
    content = content.translate(None, string.digits)
    # using regular expression to remove stopping words
    content = pattern.sub('', content)

    example_words = nltk.word_tokenize(content)
    example_words = [word for word in example_words if len(word) < 14]
    for i in range(0, len(example_words)):
        example_words[i] = porter.stem(example_words[i])
        example_words[i] = example_words[i].lower()
    vocabulary.union(example_words)
    return example_words

def process_header(header):
    lines = header.split('\n')
    header_components = {}
    for line in lines:
        components = line.split(": ")
        if components[0] == "Date":
            header_components["Date"] = components[1]
            continue
        if components[0] == "Subject":
            header_components["Subject"] = components[1]
            continue
        if components[0] == "X-From":
            header_components["X-From"] = components[1]
            continue
        if components[0] == "X-To":
            header_components["X-To"] = components[1]
            continue
        if components[0] == "X-cc":
            header_components["X-cc"] = components[1]
            continue
        if components[0] == "X-bcc":
            header_components["X-bcc"] = components[1]
            continue
        if components[0] == "X-Origin":
            header_components["X-Origin"] = components[1]
            continue
    try:
        header_components["X-To"] = process_names(header_components["X-To"])
    except KeyError:
        header_components["X-To"] = []
    try:
        header_components["X-cc"] = process_names(header_components["X-cc"])
    except KeyError:
        header_components["X-cc"] = []
    try:
        header_components["X-bcc"] = process_names(header_components["X-bcc"])
    except KeyError:
        header_components["X-bcc"] = []


    return header_components

def take_note(header_words):
    email = metadata()
    try:
        email.name = header_words['X-From']
    except KeyError:
        email.name = ""
    try:
        email.date = header_words['Date']
    except KeyError:
        email.date = ""
    try:
        email.subject = header_words['Subject']
    except KeyError:
        email.subject = ""
    try:
        email.to = header_words["X-To"]
    except KeyError:
        email.to = []
    try:
        email.cc = header_words["X-cc"]
    except KeyError:
        email.cc = []
    try:
        email.bcc = header_words["X-bcc"]
    except KeyError:
        email.bcc = []
    try:
        email.origin = header_words["X-Origin"]
    except KeyError:
        email.origin = ""
    return email

def process_single_file(file_path):
    delimiter = ".nsf"
    with open(file_path) as d:
        email = metadata()
        components = d.read().split(delimiter)
        header = components[0] + delimiter
        content = components[1]
        header_words = process_header(header)
        content_words = process_content(content)

        email = take_note(header_words)
        email.filepath = file_path
        email.content_length = len(content)
        email.total_length = len(header) + email.content_length
        email.content = content_words
        email.vocabulary = set(content_words)
        return email

# def write_emails(emails, path):
#     file = open(path + "emails", 'w')
#     for em in emails:
#         file.write(em.name + )


def process_folder(path):
    path_documents = path
    filepath_list = os.listdir(path_documents)

    emails = []
    for i in range(0, len(filepath_list)):
        if filepath_list[i][0] == '.':
            pass
        else:
            file_path = path_documents + "/" + filepath_list[i]
            email = process_single_file(file_path)
            if len(email.content) < 100:
                continue
            else:
                emails.append(email)
                vocabulary.update(email.vocabulary)

    # print vocabulary

    return emails

#################################################################

#if __name__ == "__main__":
#    path = "test_all_documents"
#    emails = process_folder(path)
