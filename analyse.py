import random
import MySQLdb as mdb
import sys

con = mdb.connect('localhost', 'root', 'bdd', 'fp');

cur = con.cursor(mdb.cursors.DictCursor)
cur.execute('SELECT counter, id , count(*) AS nbFps FROM fpData where counter > 50000 AND id != "Not supported" GROUP BY id HAVING count(id) > 1')  
multId = cur.fetchall()

print("counter~~~id~~~time~~~addressHttp~~~userAgentHttp~~~acceptHttp~~~hostHttp~~~connectionHttp~~~encodingHttp~~~languageHttp~~~orderHttp~~~pluginsJS~~~platformJS~~~cookiesJS~~~dntJS~~~timezoneJS~~~resolutionJS~~~localJS~~~sessionJS~~~IEDataJS~~~fontsFlash~~~resolutionFlash~~~languageFlash~~~platformFlash~~~adBlock~~~canvasJSHashed")
for ids in multId:
	cur.execute('SELECT counter, id, time, addressHttp, userAgentHttp, acceptHttp, hostHttp, connectionHttp, encodingHttp, languageHttp, orderHttp, pluginsJS, platformJS, cookiesJS, dntJS, timezoneJS, resolutionJS, localJS, sessionJS, IEDataJS, fontsFlash, resolutionFlash, languageFlash, platformFlash, adBlock, canvasJSHashed FROM fpData WHERE id=\"'+ids["id"]+'\" ORDER BY time')
	fps = cur.fetchall()
	for fp in fps:
		print (str(fp["counter"])+"~~~"+fp["id"]+"~~~"+str(fp["time"])+"~~~"+fp["addressHttp"]+"~~~"+fp["userAgentHttp"]+"~~~"+fp["acceptHttp"]+"~~~"+fp["hostHttp"]+"~~~"+fp["connectionHttp"]+"~~~"+fp["encodingHttp"]+"~~~"+fp["languageHttp"]+"~~~"+fp["orderHttp"]+"~~~"+fp["pluginsJS"]+"~~~"+fp["platformJS"]+"~~~"+fp["cookiesJS"]+"~~~"+fp["dntJS"]+"~~~"+fp["timezoneJS"]+"~~~"+fp["resolutionJS"]+"~~~"+fp["localJS"]+"~~~"+fp["sessionJS"]+"~~~"+fp["IEDataJS"]+"~~~"+fp["fontsFlash"]+"~~~"+fp["resolutionFlash"]+"~~~"+fp["languageFlash"]+"~~~"+fp["platformFlash"]+"~~~"+fp["adBlock"]+"~~~"+fp["canvasJSHashed"])








con.close()

random.seed(45)