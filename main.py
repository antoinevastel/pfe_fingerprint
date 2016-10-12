from Fingerprint import Fingerprint
from Data import Data
from Algorithm import Algorithm

def main():
	d = Data(computeSamples = False)
	trainIndices, testIndices = d.splitData()
	algo = Algorithm(d.getTrainSample(), d.getTestSample())
	# algo.computeRegressionInput()
	# algo.predictXGboost()
	algo.predictNN()
	# algo.predict()
	algo.writeSubmission()
	print(algo.evalPrecision())


if __name__ == "__main__":
    main()
