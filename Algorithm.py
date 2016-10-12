from Fingerprint import Fingerprint
import csv
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

class Algorithm():

	def __init__(self, trainSet, testSet):
		self.trainSet = trainSet
		self.testSet = testSet
		self.dicResTrain = dict()
		self.predictions = dict()

	def computeSimilirarity(self, fpFixed, fpCompared):
		if fpFixed.belongToSameUser(fpCompared):
			result = "0,"
		else:
			result ="1,"
		#We start with the http header attributes
		#We test if the 2 fingerprints have the same browser
		if fpFixed.hasSameBrowser(fpCompared):
			result += "0,"
		else:
			result += "1,"

		#We test if they have the same OS
		if fpFixed.hasSameOs(fpCompared):
			result += "0,"
		else:
			result += "1,"

		#We test if the version of the browser is greater or equal
		if fpFixed.hasHighestBrowserVersion(fpCompared):
			result += "0,"
		else:
			result += "1,"

		if fpFixed.hasSameHttpLanguages(fpCompared):
			result += "0,"
		else:
			result += "1,"

		if fpFixed.hasSameAcceptHttp(fpCompared):
			result += "0,"
		else:
			result += "1,"

		if fpFixed.hasSameEncodingHttp(fpCompared):
			result += "0,"
		else:
			result += "1,"

		# if fpFixed.hasSameAddressHttp(fpCompared):
		# 	result += "0,"
		# else:
		# 	result += "1,"
		#Javascript attributes
		#If one or more of the two fingerprints doesn't have javascript activated
		if not(fpFixed.hasJsActivated()) or not(fpCompared.hasJsActivated()):
			result += "2,2,2,2,2,2,2,2,2,2,"
		else:
			#We test if they have the same timezone
			if fpFixed.hasSameTimezone(fpCompared):
				result += "0,"
			else:
				result += "1,"

			#We test if the list of plugins of one of the fingerprint is the subset of the list
			#of plugins of the other fingerprint
			if fpFixed.arePluginsSubset(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameResolution(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameAdblock(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSamePlugins(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameCanvasJsHashed(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSamePlatformJs(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameDnt(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameCookie(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameLocal(fpCompared):
				result += "0,"
			else:
				result += "1,"


		#Flash attributes
		#If one or more of the two fingerprints doesn't have flash activated
		if not(fpFixed.hasFlashActivated()) or not(fpCompared.hasFlashActivated()):
			if fpFixed.hasSameFlashBlocked(fpCompared):
				result += "0,"
			else:
				result +="1,"

			result += "2,2,2,2"
		else:
			result += "2," #For the test hasSameFlashBlocked 

			#We test if the list of fonts of one of the fingerprint is the subset of the list
			#of fonts of the other fingerprint
			if fpFixed.areFontsSubset(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameFonts(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSamePlatformFlash(fpCompared):
				result += "0,"
			else:
				result += "1,"

			if fpFixed.hasSameResolutionFlash(fpCompared):
				result += "0"
			else:
				result += "1"

		return result

	def computeRegressionInput(self):
		print("Start computeRegressionInput")
		#result is the string describing the results from all the points we are going to test
		#to compare two fingerprints

		#We compare every fingerprints with all the other except itself
		f = open("./samples/regInput.csv", 'w')
		f.write("sameUser,browser,os,browserVersion,httpLanguages,acceptHttp,encodingHttp,timezoneJs,pluginsSubset,resolutionJs,adblock,plugins,canvasJs,platformJs,dntJs,cookiesJs,localJs,flashBlockedExt,fontsSubset,fonts,platformFlash,resolutionFlash\n")
		for i in range(len(self.trainSet)):
			if i % 500 == 0:
				print(i)
			fpFixed = self.trainSet[i]
			for j in range(i+1, len(self.trainSet)):
				fpCompared = self.trainSet[j]
				if fpFixed.id == fpCompared.id:
					result = self.computeSimilirarity(fpFixed, fpCompared)
					f.write(result+"\n")

		for i in range(len(self.trainSet)):
			if i % 500 ==0:
				print(i)
			# compareWith = random.randint(250, 350)
			compareWith = random.randint(50, 100)
			fpFixed = self.trainSet[i]
			for j in range(i+1, len(self.trainSet)):
				fpCompared = self.trainSet[j]
				if j%compareWith == 0 and fpFixed.id != fpCompared.id:
					result = self.computeSimilirarity(fpFixed, fpCompared)
					f.write(result+"\n")
		
		f.close()

	def predict(self):
		print("Start Predict")
		df = pd.read_csv("./samples/regInput.csv")
		cols = df.columns.tolist()

		y = df[cols[0]]  # variable to predict
		X = df[cols[1:]]
		y = np.ravel(y)
		# model = LogisticRegression(n_jobs = 3)
		model = RandomForestClassifier(n_estimators=5, n_jobs=3)
		model = model.fit(X, y)

		cpt = 0
		for fpTest in self.testSet:
			print(cpt)
			cpt += 1
			f = open("./samples/regInputPred.csv", 'w')
			f.write("sameUser,browser,os,browserVersion,httpLanguages,acceptHttp,encodingHttp,timezoneJs,pluginsSubset,resolutionJs,adblock,plugins,canvasJs,platformJs,dntJs,cookiesJs,localJs,flashBlockedExt,fontsSubset,fonts,platformFlash,resolutionFlash\n")
			for fpTrain in self.trainSet:
				resultComparaison = self.computeSimilirarity(fpTest, fpTrain)
				f.write(resultComparaison + "\n")

			f.close()
			dfPredict = pd.read_csv("./samples/regInputPred.csv")
			cols = dfPredict.columns.tolist()
			yp = dfPredict[cols[0]]
			Xp = dfPredict[cols[1:]]
			predicted = model.predict_proba(Xp)

			nearest = (-predicted[:, 0]).argsort()[:30]

			if predicted[nearest[0], 0] > 0.93:
				self.predictions[fpTest.counter] = self.trainSet[nearest[0]].id
			else:
				self.predictions[fpTest.counter] = None

			res = fpTest.id == self.trainSet[nearest[0]].id
			print(
				"Prediction : " + str(fpTest.counter) + " ," + str(self.predictions[fpTest.counter]) + ", " + str(res))

	def predictXGboost(self):
		print("Start Predict")
		df = pd.read_csv("./samples/regInput.csv")
		cols = df.columns.tolist()

		y = df[cols[0]]  # variable to predict
		le = LabelEncoder()
		y = le.fit_transform(y)

		X = df[cols[1:]]
		y = np.ravel(y)

		train_X = X.as_matrix()
		# train_y = y.as_matrix()
		gbm = xgb.XGBClassifier(max_depth=5, n_estimators=250, learning_rate=0.05).fit(train_X, y)

		cpt = 0
		for fpTest in self.testSet:
			print(cpt)
			cpt += 1
			f = open("./samples/regInputPred.csv", 'w')
			f.write("sameUser,browser,os,browserVersion,httpLanguages,acceptHttp,encodingHttp,timezoneJs,pluginsSubset,resolutionJs,adblock,plugins,canvasJs,platformJs,dntJs,cookiesJs,localJs,flashBlockedExt,fontsSubset,fonts,platformFlash,resolutionFlash\n")
			for fpTrain in self.trainSet:
				resultComparaison = self.computeSimilirarity(fpTest, fpTrain)
				f.write(resultComparaison + "\n")

			f.close()
			dfPredict = pd.read_csv("./samples/regInputPred.csv")
			cols = dfPredict.columns.tolist()
			yp = dfPredict[cols[0]]
			Xp = dfPredict[cols[1:]]
			predicted = gbm.predict_proba(Xp.as_matrix())

			nearest = (-predicted[:, 0]).argsort()[:30]

			if predicted[nearest[0], 0] > 0.93:
				self.predictions[fpTest.counter] = self.trainSet[nearest[0]].id
			else:
				self.predictions[fpTest.counter] = None

			res = fpTest.id == self.trainSet[nearest[0]].id
			print(
				"Prediction : " + str(fpTest.counter) + " ," + str(self.predictions[fpTest.counter]) + ", " + str(res))

	def predictNN(self):
		print("Start Predict")
		df = pd.read_csv("./samples/regInput.csv")
		cols = df.columns.tolist()

		y = df[cols[0]]  # variable to predict
		le = LabelEncoder()
		y = le.fit_transform(y)

		X = df[cols[1:]]
		y = np.ravel(y)

		train_X = X.as_matrix()
		#22,2 -> 0.763
		#23,2 -> 0.786
		#24,2 -> 0.783
		clf = MLPClassifier(activation="logistic", solver='lbfgs', alpha=1e-3, hidden_layer_sizes=(5, 5, 2), random_state=1)
		clf.fit(X, y)

		cpt = 0
		for fpTest in self.testSet:
			print(cpt)
			cpt += 1
			f = open("./samples/regInputPred.csv", 'w')
			f.write("sameUser,browser,os,browserVersion,httpLanguages,acceptHttp,encodingHttp,timezoneJs,pluginsSubset,resolutionJs,adblock,plugins,canvasJs,platformJs,dntJs,cookiesJs,localJs,flashBlockedExt,fontsSubset,fonts,platformFlash,resolutionFlash\n")
			for fpTrain in self.trainSet:
				resultComparaison = self.computeSimilirarity(fpTest, fpTrain)
				f.write(resultComparaison + "\n")

			f.close()
			dfPredict = pd.read_csv("./samples/regInputPred.csv")
			cols = dfPredict.columns.tolist()
			yp = dfPredict[cols[0]]
			Xp = dfPredict[cols[1:]]
			predicted = clf.predict_proba(Xp.as_matrix())

			nearest = (-predicted[:, 0]).argsort()[:30]
			#0.93 original
			if predicted[nearest[0], 0] > 0.90:
				self.predictions[fpTest.counter] = self.trainSet[nearest[0]].id
			else:
				self.predictions[fpTest.counter] = None

			res = fpTest.id == self.trainSet[nearest[0]].id
			print("Prediction : " + str(fpTest.counter) + " ," + str(self.predictions[fpTest.counter]) + ", " + str(res))

	def writeSubmission(self):
		if len(self.predictions) == 0:
			self.predict()

		f = open("./samples/submission.csv", 'w')
		for counter in self.predictions:
			f.write(str(counter)+","+str(self.predictions[counter])+"\n")	

	def evalPrecision(self):
		idsTrain = set()
		for fp in self.trainSet:
			idsTrain.add(fp.id)

		with open('./samples/submission.csv', 'r') as submissionFile:
			submissionReader = csv.reader(submissionFile, delimiter=',')
			for row in submissionReader:
				self.predictions[int(row[0])] = row[1]

		precision = 0.0
		noneError = 0.0
		badIdError = 0.0
		for fpTest in self.testSet:
			if self.predictions[fpTest.counter] == fpTest.id:
				precision += 1.0
			elif self.predictions[fpTest.counter] == "None" and fpTest.id not in idsTrain:
				precision += 1.0
			elif self.predictions[fpTest.counter] == "None" and fpTest.id in idsTrain:
				noneError += 1.0
			elif self.predictions[fpTest.counter] != fpTest.id:
				badIdError += 1.0

		print("noneError : " + str(noneError / float(len(self.testSet))))
		print("badIdError : " + str(badIdError / float(len(self.testSet))))
		return precision / float(len(self.testSet))







