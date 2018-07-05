from pyspark.mllib.util import MLUtils
from pyspark import SparkContext, SparkConf
from pyspark.ml.clustering import LDA
from pyspark.sql import SparkSession
from pyspark.ml.feature import SQLTransformer
import os
# Loads data.
# print "\n", os.path.isdir("svmVector"), "\n"
spark = SparkSession.builder.master("local[*]").getOrCreate()
dataset = spark.read.format("libsvm").load("vectors/svm")

# Trains a LDA model.
lda = LDA(k=10, maxIter=10)
model = lda.fit(dataset)

ll = model.logLikelihood(dataset)
lp = model.logPerplexity(dataset)
print("The lower bound on the log likelihood of the entire corpus: " + str(ll))
print("The upper bound bound on perplexity: " + str(lp))

# Describe topics.
topics = model.describeTopics(3)
print("The topics described by their top-weighted terms:")
topics.show(truncate=False)

# Shows the result
transformed = model.transform(dataset)
tiqu = transformed.select("topicDistribution")
# transformed.show(truncate=False)
a = tiqu.head(100000)
file_res = open("vectors/topics", 'w')
for x in a:
    for n in x:
        file_res.write(','.join(str(j) for j in n))
    file_res.write('\n')
file_res.close()
