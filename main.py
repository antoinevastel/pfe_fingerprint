from Fingerprint import Fingerprint
import MySQLdb as mdb
from Data import Data
from Algorithm import Algorithm

def main():
	d = Data(computeSamples = False)
	trainIndices, testIndices = d.splitData()
	algo = Algorithm(d.getTrainSample(), d.getTestSample())
	#algo.computeRegressionInput()
	algo.predictNN()
	# algo.writeSubmission()
	# print algo.evalPrecision()


if __name__ == "__main__":
    main()
