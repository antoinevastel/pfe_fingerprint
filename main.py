from Fingerprint import Fingerprint
import MySQLdb as mdb
from Data import Data
from Algorithm import Algorithm

def main():
	# con = mdb.connect('localhost', 'root', 'bdd', 'fp');
	# cur = con.cursor(mdb.cursors.DictCursor)
	d = Data(computeSamples = False)
	trainIndices, testIndices = d.splitData()
	algo = Algorithm(d.getTrainSample(), d.getTestSample())


if __name__ == "__main__":
    main()
