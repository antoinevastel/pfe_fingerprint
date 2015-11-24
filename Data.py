import MySQLdb as mdb
import csv
import random
from sklearn.cross_validation import train_test_split

class Data():
	def __init__(self, seed = 42):
		self.seed = seed
		random.seed(seed)
		self.con = mdb.connect('localhost', 'root', 'bdd', 'fp');
		self.cur = self.con.cursor(mdb.cursors.DictCursor)

	def splitData(self, computeSamples = False):
		if computeSamples:
			self.cur.execute('SELECT id , count(*) AS nbFps FROM fpData where id != "Not supported" GROUP BY id HAVING count(id) > 1')  
			multId = self.cur.fetchall()
			total = list()
			cpt = 0
			for ids in multId:
				if cpt%100 == 0:
					print cpt
				cpt += 1
				self.cur.execute('SELECT counter from fpData WHERE id=\"'+ids["id"]+'\"')
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
					train.append(int(row[0]))

			with open("/home/avastel/prog/pfe/test.csv", 'rb') as trainFile:
				testReader = csv.reader(testFile, delimiter=',')
				for counter in testReader:
					test.append(int(row[0]))

		return train, test



