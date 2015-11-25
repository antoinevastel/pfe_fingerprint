import MySQLdb as mdb
import csv
import random
from sklearn.cross_validation import train_test_split
from Fingerprint import Fingerprint

class Data():
	def __init__(self, computeSamples = False, seed = 42):
		self.seed = seed
		random.seed(seed)
		self.con = mdb.connect('localhost', 'root', 'bdd', 'fp');
		self.cur = self.con.cursor(mdb.cursors.DictCursor)
		self.train = list()
		self.test = list()
		self.computeSamples= computeSamples

	def splitData(self):
		if self.computeSamples:
			self.cur.execute('SELECT id , count(*) AS nbFps FROM fpData where id != "Not supported" GROUP BY id HAVING count(id) > 1')  
			multId = self.cur.fetchall()
			total = list()


			idString = "("
			for ids in multId:
				idString += str(ids["id"])+","
			counterString = counterString[0: len(counterString)-1]
			counterString += ")"

			self.cur.execute('SELECT counter from fpData WHERE id in '+idString)
			counters = self.cur.fetchall()
			for counter in counters:
				total.append(counter["counter"])

			#we keep 20% of these counters for the test, the others go in the train
			train, test = train_test_split(total, train_size = 0.8)
			#we get users with only 1 fingerprint
			self.cur.execute('SELECT counter, id , count(*) AS nbFps FROM fpData where id != "Not supported" GROUP BY id HAVING count(id) = 1')
			singleFps = set()
			singId = self.cur.fetchall()
			cpt = 0
			for ids in singId:
				if cpt % 100 == 0:
					print cpt
				cpt += 1
				singleFps.add(ids["counter"])

			singleFpsSelected = random.sample(singleFps, len(test))
			test = test + singleFpsSelected


			f = open("/home/avastel/prog/pfe/train.csv", 'w')
			for counter in train:
				f.write(str(counter)+"\n")

			f = open("/home/avastel/prog/pfe/test.csv", 'w')
			for counter in test:
				f.write(str(counter)+"\n")
		else:
			train = list()
			test = list()
			with open("/home/avastel/prog/pfe/train.csv", 'rb') as trainFile:
				trainReader = csv.reader(trainFile, delimiter=',')
				for counter in trainReader:
					train.append(int(counter[0]))

			with open("/home/avastel/prog/pfe/test.csv", 'rb') as testFile:
				testReader = csv.reader(testFile, delimiter=',')
				for counter in testReader:
					test.append(int(counter[0]))

		self.train = train
		self.test = test

		return train, test

	def getTrainSample(self):
		if len(self.train) == 0:
			self.splitData()

		counterString = "("
		for counter in self.train:
			counterString += str(counter)+","

		counterString = counterString[0: len(counterString)-1]
		counterString += ")"
		self.cur.execute('SELECT counter, id, addressHttp, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, canvasJSHashed FROM fpData WHERE counter in '+counterString)
		res = self.cur.fetchall()

		trainSet = list()
		for v in res:
			trainSet.append(Fingerprint(v))

		return trainSet

	def getTestSample(self):
		if len(self.test) == 0:
			self.splitData()

		counterString = "("
		for counter in self.test:
			counterString += str(counter)+","

		counterString = counterString[0: len(counterString)-1]
		counterString += ")"
		self.cur.execute('SELECT counter, id, addressHttp, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, canvasJSHashed FROM fpData WHERE counter in '+counterString)
		res =  self.cur.fetchall()
		
		testSet = list()
		for v in res:
			testSet.append(Fingerprint(v))

		return testSet


