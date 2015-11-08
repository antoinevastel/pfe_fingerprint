import random
import MySQLdb as mdb
import sys

con = mdb.connect('localhost', 'root', 'bdd', 'fp');

cur = con.cursor(mdb.cursors.DictCursor)
#we get the id of all the users having at least 2 fingerprints
cur.execute('SELECT id , count(*) AS nbFps FROM fpData where id != "Not supported" GROUP BY id HAVING count(id) > 1')  
multId = cur.fetchall()

#probabilityChange is the dict{attribute => probability to change}
probabilityChange = dict()
#initialization of probabilityChange
probabilityChange["addressHttp"] = 0.0
probabilityChange["userAgentHttp"] = 0.0
probabilityChange["acceptHttp"] = 0.0
probabilityChange["hostHttp"] = 0.0
probabilityChange["connectionHttp"] = 0.0
probabilityChange["encodingHttp"] = 0.0
probabilityChange["languageHttp"] = 0.0
probabilityChange["orderHttp"] = 0.0
probabilityChange["pluginsJS"] = 0.0
probabilityChange["platformJS"] = 0.0
probabilityChange["cookiesJS"] = 0.0
probabilityChange["dntJS"] = 0.0
probabilityChange["timezoneJS"] = 0.0
probabilityChange["resolutionJS"] = 0.0
probabilityChange["localJS"] = 0.0
probabilityChange["sessionJS"] = 0.0
probabilityChange["IEDataJS"] = 0.0
probabilityChange["fontsFlash"] = 0.0
probabilityChange["resolutionFlash"] = 0.0
probabilityChange["languageFlash"] = 0.0
probabilityChange["platformFlash"] = 0.0
probabilityChange["adBlock"] = 0.0
probabilityChange["canvasJSHashed"] = 0.0

nbFingerprints = 0.0 
for ids in multId:
	#print ids["id"], ids["nbFps"]
	#for every user with at least 2 fingerprints we retrieve all its fingerprints and sort them chronologically
	cur.execute('SELECT counter, id, time, addressHttp, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, canvasJSHashed FROM fpData WHERE id=\"'+ids["id"]+'\" ORDER BY time')
	fps = cur.fetchall()
	first = True
	for fp in fps:
		if first == True:
			previousFp = fp
			first = False
		else:
			currentFp = fp
			#we compare the current fingerprint with the previous one (chronologically speaking) and we add 1 
			#to probabablityChange[att] if there is a difference between previousFp[att] and currentFp[att]
			for attribute in probabilityChange:
				if currentFp[attribute] != previousFp[attribute]:
					probabilityChange[attribute] += 1

			#The current fingerprint becomes the previous one
			previousFp = currentFp

	#nbFingerprints is not really equal to the number of fingerprints
	#it's equal to the maximum number of changes that could occur on our whole dataset
	#For example example, if we consider only 4 fingerprints, only 3 changes can happen
	#More generally if for every id we have n fingerprints, n-1 max changes can happen
	nbFingerprints += len(fps) - 1
	print nbFingerprints

for attribute in probabablityChange:
	probabablityChange[attribute] /= nbFingerprints
	print attribute, probabilityChange[attribute]

con.close()