from Fingerprint import Fingerprint

class Algorithm():

	def __init__(self, trainSet, testSet):
		self.trainSet = trainSet
		self.testSet = testSet

	def trainAlgoV1(self):
		#result is the string describing the results from all the points we are going to test
		#to compare two fingerprints

		result = ""
		#We compare every fingerprints with all the other except itself
		for i in range(len(trainSet)):
			fpFixed = trainSet[i]
			for j in range(i+1, len(trainSet)):
				result = ""
				fpCompared = trainSet[j]

				#We start with the http header attributes
				#We test if the 2 fingerprints have the same browser
				if fpFixed.hasSameBrowser(fpCompared):
					result += "0"
				else:
					result += "1"

				#We test if they have the same OS
				if fpFixed.hasSameOs(fpCompared):
					result += "0"
				else:
					result += "1"

				#We test if the version of the browser is greater or equal
				if fpFixed.hasHighestBrowserVersion(fpCompared):
					result += "0"
				else:
					result += "1"

				if fpFixed.hasSameHttpLanguages(fpCompared):
					result += "0"
				else:
					result += "1"

				#Javascript attributes
				#If one or more of the two fingerprints doesn't have javascript activated
				if not(fpFixed.hasJsActivated() or fpCompared.hasJsActivated()):
					result += "22222"
				else:
					#We test if they have the same timezone
					if fpFixed.hasSameTimezone(fpCompared):
						result += "0"
					else:
						result += "1"

					#We test if the list of plugins of one of the fingerprint is the subset of the list
					#of plugins of the other fingerprint
					if fpFixed.arePluginsSubset(fpCompared):
						result += "0"
					else:
						result += "1"

					if fpFixed.hasSameResolution(fpCompared):
						result += "0"
					else:
						result += "1"

					if fpFixed.hasSameResolution(fpCompared):
						result += "0"
					else:
						result += "1"

					if fpFixed.hasSameAdblock(fpCompared):
						result += "0"
					else:
						result += "1"

				#Flash attributes
				#If one or more of the two fingerprints doesn't have flash activated
				if not(fpFixed.hasFlashActivated() or fpCompared.hasFlashActivated()):
					result += "2"
				else:
					#We test if the list of fonts of one of the fingerprint is the subset of the list
					#of fonts of the other fingerprint
					if fpFixed.areFontsSubset(fpCompared):
						result += "0"
					else:
						result += "1"


