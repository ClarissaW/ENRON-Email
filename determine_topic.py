file = open("vectors/topics", 'r')
td = file.readlines()
file.close()
print td[0]
topic = []
for line in td:
    line = line.strip('\n')
    line = line.split(',')
    for i in range(0, len(line)):
        line[i] = float(line[i])
    maximum = max(line)
    topic.append(line.index(maximum))

print topic

file = open("vectors/topic_for_mail", 'w')
for i in range(0, len(topic)):
    file.write(str(i + 1) + ": " + str(topic[i]) + "\n")
file.close()