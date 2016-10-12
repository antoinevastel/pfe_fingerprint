import random
import MySQLdb as mdb
import sys
import re

def getUsersWithMultipesFp(cur):
	#we get the id of all the users having at least 2 fingerprints
	cur.execute('SELECT id , count(*) AS nbFps FROM fpData where id != "Not supported" GROUP BY id HAVING count(id) > 1')  
	return cur.fetchall()

def computeProbabilityChange(cur, multId):
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
		print(nbFingerprints)

	for attribute in probabilityChange:
		probabilityChange[attribute] /= nbFingerprints
		print(attribute, probabilityChange[attribute])


def computeProbabilityNbPluginsChanges(cur, multId):
	nbFingerprints = 0.0
	pIncrease = 0.0
	pDecrease = 0.0 
	for ids in multId:
		#for every user with at least 2 fingerprints we retrieve all its fingerprints and sort them chronologically
		cur.execute('SELECT counter, id, time, pluginsJS FROM fpData WHERE id=\"'+ids["id"]+'\" ORDER BY time')
		fps = cur.fetchall()
		first = True
		for fp in fps:
			if first == True:
				previousFp = fp
				first = False
			else:
				currentFp = fp
				#we compare the number of plugins of the current fingerprint with the previous one (chronologically speaking)
				nbPluginsCurrent = len(re.findall("Plugin [0-9]+: ([a-zA-Z -.]+)", currentFp["pluginsJS"]))
				nbPluginsPrevious = len(re.findall("Plugin [0-9]+: ([a-zA-Z -.]+)", previousFp["pluginsJS"]))

				print(nbPluginsCurrent, nbPluginsPrevious)

				if nbPluginsCurrent > nbPluginsPrevious:
					pIncrease += 1.0
				elif nbPluginsCurrent < nbPluginsPrevious:
					pDecrease += 1.0

				#The current fingerprint becomes the previous one
				previousFp = currentFp

		#nbFingerprints is not really equal to the number of fingerprints
		#it's equal to the maximum number of changes that could occur on our whole dataset
		#For example example, if we consider only 4 fingerprints, only 3 changes can happen
		#More generally if for every id we have n fingerprints, n-1 max changes can happen
		nbFingerprints += float(len(fps)) - 1.0
		print(nbFingerprints)

	pIncrease = pIncrease / nbFingerprints
	pDecrease = pDecrease / nbFingerprints
	pNoChange = 1 -(pIncrease + pDecrease)

	print(pIncrease, pDecrease, pNoChange)

def computeProbabilityTurnOffFlash(cur, multId):
	nbFingerprints = 0.0
	pChangeLanguage = 0.0
	pChangeResolution = 0.0
	pChangePlatform = 0.0

	nd = "Flash not detected"
	d = "Flash detected but not activated (click-to-play)"
	for ids in multId:
		#for every user with at least 2 fingerprints we retrieve all its fingerprints and sort them chronologically
		cur.execute('SELECT counter, id, time, platformFlash, resolutionFlash, languageFlash FROM fpData WHERE id=\"'+ids["id"]+'\" ORDER BY time')
		fps = cur.fetchall()
		first = True
		for fp in fps:
			if first == True:
				previousFp = fp
				first = False
			else:
				currentFp = fp

				if ((currentFp["platformFlash"] == nd or currentFp["platformFlash"] == d) and \
				(previousFp["platformFlash"] != nd and previousFp["platformFlash"] != d)) or \
				((currentFp["platformFlash"] != nd and currentFp["platformFlash"] != d) and \
				(previousFp["platformFlash"] == nd or previousFp["platformFlash"] == d)):
					pChangePlatform += 1.0

				if ((currentFp["resolutionFlash"] == nd or currentFp["resolutionFlash"] == d) and \
				(previousFp["resolutionFlash"] != nd and previousFp["resolutionFlash"] != d)) or \
				((currentFp["resolutionFlash"] != nd and currentFp["resolutionFlash"] != d) and \
				(previousFp["resolutionFlash"] == nd or previousFp["resolutionFlash"] == d)):
					pChangeResolution += 1.0

				if ((currentFp["languageFlash"] == nd or currentFp["languageFlash"] == d) and \
				(previousFp["languageFlash"] != nd and previousFp["languageFlash"] != d)) or \
				((currentFp["languageFlash"] != nd and currentFp["languageFlash"] != d) and \
				(previousFp["languageFlash"] == nd or previousFp["languageFlash"] == d)):
					pChangeLanguage += 1.0


				#The current fingerprint becomes the previous one
				previousFp = currentFp

		#nbFingerprints is not really equal to the number of fingerprints
		#it's equal to the maximum number of changes that could occur on our whole dataset
		#For example example, if we consider only 4 fingerprints, only 3 changes can happen
		#More generally if for every id we have n fingerprints, n-1 max changes can happen
		nbFingerprints += float(len(fps)) - 1.0
		print(nbFingerprints)

	pChangePlatform = pChangePlatform / nbFingerprints
	pChangeResolution = pChangeResolution / nbFingerprints
	pChangeLanguage = pChangeLanguage / nbFingerprints

	print(pChangePlatform, pChangeResolution, pChangeLanguage)
	#0.204459765162 0.204459765162 0.204459765162

def computeProbabilityTurnOffJs(cur, multId):
	nbFingerprints = 0.0
	pChange = 0.0
	for ids in multId:
	#for every user with at least 2 fingerprints we retrieve all its fingerprints and sort them chronologically
		cur.execute('SELECT counter, id, time, platformJS FROM fpData WHERE id=\"'+ids["id"]+'\" ORDER BY time')
		fps = cur.fetchall()
		first = True
		for fp in fps:
			if first == True:
				previousFp = fp
				first = False
			else:
				currentFp = fp

				if (currentFp["platformJS"] == "no JS" and previousFp["platformJS"] != "no JS") or \
				(currentFp["platformJS"] != "no JS" and previousFp["platformJS"] == "no JS"):
					pChange += 1.0

				previousFp = currentFp

		nbFingerprints += float(len(fps)) - 1.0
		print(nbFingerprints)

	pChange = pChange / nbFingerprints
	print(pChange)
	# 0.0411622276029

def computeChangesFonts(cur, multId):
	nbFingerprints = 0.0
	pIncrease = 0.0
	pDecrease = 0.0
	nd = "Flash not detected"
	d = "Flash detected but not activated (click-to-play)" 
	for ids in multId:
		#for every user with at least 2 fingerprints we retrieve all its fingerprints and sort them chronologically
		cur.execute('SELECT counter, id, time, fontsFlash FROM fpData WHERE id=\"'+ids["id"]+'\" AND fontsFlash !=\"'+nd+'\" AND fontsFlash !=\"'+d+'\" ORDER BY time')
		fps = cur.fetchall()
		first = True
		for fp in fps:
			if first == True:
				previousFp = fp
				first = False
			else:
				currentFp = fp
				#we compare the number of plugins of the current fingerprint with the previous one (chronologically speaking)
				nbFontsCurrent = len(currentFp["fontsFlash"].split("_"))
				nbFontsPrevious = len(previousFp["fontsFlash"].split("_"))

				if nbFontsCurrent > nbFontsPrevious:
					pIncrease += 1.0
				elif nbFontsCurrent < nbFontsPrevious:
					pDecrease += 1.0

				#we increase nbFingerprints only if there are at least 2 fp with flash activated
				nbFingerprints += 1.0

				#The current fingerprint becomes the previous one
				previousFp = currentFp

		print(nbFingerprints)

	pIncrease = pIncrease / nbFingerprints
	pDecrease = pDecrease / nbFingerprints
	pNoChange = 1 -(pIncrease + pDecrease)

	print(pIncrease, pDecrease, pNoChange)
	#0.0406020301015 0.0507525376269 0.908645432272

def main():
	con = mdb.connect('localhost', 'root', 'bdd', 'fp');
	cur = con.cursor(mdb.cursors.DictCursor)
	multId = getUsersWithMultipesFp(cur)

	#We keep 66% of the id
	multIdStats = list()
	i = 0
	for indiv in multId:
		if i%2 == 0 or i%3 ==0:
			multIdStats.append(indiv)

		i += 1

	#computeProbabilityChange(cur, multId)
	#computeProbabilityNbPluginsChanges(cur, multId)
	#computeProbabilityTurnOffFlash(cur, multIdStats)
	#computeProbabilityTurnOffJs(cur, multIdStats)
	computeChangesFonts(cur, multIdStats)
	con.close()

if __name__ == "__main__":
    main()
