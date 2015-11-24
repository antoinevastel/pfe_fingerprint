from Fingerprint import Fingerprint
import MySQLdb as mdb
from Data import Data

def main():
	# con = mdb.connect('localhost', 'root', 'bdd', 'fp');
	# cur = con.cursor(mdb.cursors.DictCursor)
	# cur.execute('SELECT counter, id, time, addressHttp, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, canvasJSHashed FROM fpData WHERE counter = 63929')
	# dictFp1 = cur.fetchall()[0]
	# cur.execute('SELECT counter, id, time, addressHttp, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, canvasJSHashed FROM fpData WHERE counter = 63935')
	# dictFp2 = cur.fetchall()[0]

	# fp1 = Fingerprint(dictFp1)
	# fp2 = Fingerprint(dictFp2)

	# #we compare the 2 fingerprints
	# print "Fonts subset ? : ", fp1.areFontsSubset(fp2)
	# print "Plugins subset ? : ", fp2.arePluginsSubset(fp2) 
	# print "Plugins fp1 : ", fp1.getNumberOfPlugins()
	# print "Plugins fp2 : ", fp2.getNumberOfPlugins()
	# print "Number different plugins : ", fp1.getNumberDifferentPlugins(fp2)
	d = Data()
	train, test = d.splitData(computeSamples = False)
	print len(train), len(test)


if __name__ == "__main__":
    main()
