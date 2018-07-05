from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark import SparkContext, SparkConf
from numpy import array
from math import sqrt
import time

start_time = time.time()

sc = SparkContext('local')
# Load and parse the data
data = sc.textFile("vectors/kmeans")
parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))
# Build the model (cluster the data)
clusters = KMeans.train(parsedData, 100, maxIterations=20, initializationMode="random")
# Evaluate clustering by computing Within Set Sum of Squared Errors
def error(point):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))

WSSSE = parsedData.map(lambda point: error(point)) .reduce(lambda x, y: x + y)
print("Within Set Sum of Squared Error = " + str(WSSSE))
# # Save and load model
# # clusters.save(sc, "KMeansModel")
# # sameModel = KMeansModel.load(sc, "KMeansModel")

end_time = time.time()
elapsed = end_time - start_time
print "elapsed time: ", str(elapsed)
