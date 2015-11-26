from Fingerprint import Fingerprint
import pickle
import csv

class Algorithm():

	def __init__(self, trainSet, testSet):
		self.trainSet = trainSet
		self.testSet = testSet
		self.dicResTrain = dict()
		self.predictions = dict()

	def computeSimilirarity(self, fpFixed, fpCompared):
		result =""
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
		if not(fpFixed.hasJsActivated()) or not(fpCompared.hasJsActivated()):
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
		if not(fpFixed.hasFlashActivated()) or not(fpCompared.hasFlashActivated()):
			result += "2"
		else:
			#We test if the list of fonts of one of the fingerprint is the subset of the list
			#of fonts of the other fingerprint
			if fpFixed.areFontsSubset(fpCompared):
				result += "0"
			else:
				result += "1"

		return result

	def trainV1(self):
		print "Start trainV1"
		#result is the string describing the results from all the points we are going to test
		#to compare two fingerprints
		try:
			self.dicResTrain = pickle.load(open('./data/dicRes.p', "rb" ))
		except:
			dicRes = dict()
			#We compare every fingerprints with all the other except itself
			for i in range(len(self.trainSet)):
				print i
				fpFixed = self.trainSet[i]
				for j in range(i+1, len(self.trainSet)):
					fpCompared = self.trainSet[j]
					result = self.computeSimilirarity(fpFixed, fpCompared)
					if fpFixed.belongToSameUser(fpCompared):
						try:
							dicRes[result][0] += 1.0
						except:
							dicRes[result] = (1.0, 0.0)
					else:
						try:
							dicRes[result][1] += 1.0
						except:
							dicRes[result] = (0.0, 1.0)

			dicFinal = dict()
			for k in dicRes:
				dicFinal[k] = (dicRes[k][0] / (dicRes[k][0] + dicRes[k][1]), dicRes[k][1] / (dicRes[k][0] + dicRes[k][1]))

			pickle.dump(dicFinal, open('./data/dicRes.p', "wb" ))
			self.dicResTrain = dicFinal


	def predict(self):
		print "Start Predict"
		if len(self.dicResTrain) == 0:
			self.trainV1()

		cpt = 0
		for fpTest in self.testSet:
			print cpt
			cpt += 1
			maxProba = 0.0
			idUser = None
			for fpTrain in self.trainSet:
				resultComparaison = self.computeSimilirarity(fpTest, fpTrain)
				try:
					probas = self.dicResTrain[resultComparaison]
					if probas[0] > probas[1]:
						maxProbaTemp = probas[0]
						idUserTemp = fpTrain.id
					else:
						maxProbaTemp = probas[1]
						idUserTemp = None

					if maxProbaTemp > maxProba:
						maxProba = maxProbaTemp
						idUser = idUserTemp
				except:
					pass

			self.predictions[fpTest.counter] = idUser

	def writeSubmission(self):
		if len(self.predictions) == 0:
			self.predict()

		f = open("/home/avastel/prog/pfe/submission.csv", 'w')
		for counter in self.predictions:
			f.write(str(counter)+","+str(self.predictions[counter])+"\n")	

	def evalPrecision(self):
		idsTrain = set()
		for fp in self.trainSet:
			idsTrain.add(fp.id)

		with open('/home/avastel/prog/pfe/submission.csv', 'rb') as submissionFile:
			submissionReader = csv.reader(submissionFile, delimiter=',')
			for row in submissionReader:
				self.predictions[int(row[0])] = row[1]

		precision = 0.0
		for fpTest in self.testSet:
			if self.predictions[fpTest.counter] == fpTest.id:
				precision += 1.0
			elif self.predictions[fpTest.counter] == None and fpTest.id not in idsTrain:
				precision += 1.0

		return precision / float(len(self.testSet))







