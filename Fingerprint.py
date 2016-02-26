from ua_parser import user_agent_parser
import re

class Fingerprint():

	def __init__(self, attributes):
		self.id = attributes["id"]
		self.counter = attributes["counter"]
		self.acceptHttp = attributes["acceptHttp"]
		self.cookiesJs = attributes["cookiesJS"]
		self.languageHttp = attributes["languageHttp"]
		self.platformFlash = attributes["platformFlash"]
		self.userAgentHttp = attributes["userAgentHttp"] 
		self.orderHttp = attributes["orderHttp"]
		self.addressHttp = attributes["addressHttp"]
		self.connectionHttp = attributes["connectionHttp"]
		self.resolutionJs = attributes["resolutionJS"]
		self.fontsFlash = attributes["fontsFlash"]
		self.languageFlash = attributes["languageFlash"]
		self.adBlock = attributes["adBlock"]
		self.timezoneJs = attributes["timezoneJS"]
		self.pluginsJs = attributes["pluginsJS"]
		self.sessionJs = attributes["sessionJS"]
		self.dntJs = attributes["dntJS"]
		self.encodingHttp = attributes["encodingHttp"]
		self.resolutionFlash = attributes["resolutionFlash"]
		self.IEDataJs = attributes["IEDataJS"]
		self.hostHttp = attributes["hostHttp"]
		self.canvasJsHashed = attributes["canvasJSHashed"]
		self.localJs = attributes["localJS"]
		self.platformJs = attributes["platformJS"]
		self.nbPlugins = attributes["nbPlugins"]
		self.nbFonts = attributes["nbFonts"]
		self.os = attributes["os"]
		self.browser = attributes["browser"]
		self.browserVersion = attributes["browserVersion"]

		self.userAgentInfo = dict()
		if self.hasFlashActivated():
			self.languageInconsistency = self._hasLanguageInconsistency()
		if self.hasJsActivated():
			self.platformInconsistency = self._hasPlatformInconsistency()


	def hasJsActivated(self):
		return self.platformJs != "no JS"

	def hasFlashActivated(self):
		return (self.fontsFlash != "Flash detected but not activated (click-to-play)" and self.fontsFlash != "Flash not detected" and self.fontsFlash !="Flash detected but blocked by an extension")

	def getFonts(self):
		if self.hasFlashActivated():
			return self.fontsFlash.split("_")
		else:
			raise ValueError("Flash is not activated")

	def getNumberFonts(self):
		if self.hasFlashActivated():
			return len(self.fontsFlash.split("_"))
		else:
			raise ValueError("Flash is not activated")

	def getPlugins(self):
		if self.hasJsActivated():
			return re.findall("Plugin [0-9]+: ([a-zA-Z -.]+)", self.pluginsJs)
		else:
			raise ValueError("Javascript is not activated")

	def getNumberOfPlugins(self):
		return self.nbPlugins

	def getBrowser(self):
		return self.browser

	def getOs(self):
		return self.os

	def _hasLanguageInconsistency(self):
		if self.hasFlashActivated():
			try:
				langHttp = self.languageHttp[0:2].lower()
				langFlash = self.languageFlash[0:2].lower()
				return not(langHttp == langFlash)
			except:
				return True
		else:
			raise ValueError("Flash is not activated")

	def _hasPlatformInconsistency(self):
		if self.hasJsActivated():
			try:
				platUa = self.getOs()[0:3].lower()
				if self.hasFlashActivated():
					platFlash = self.platformFlash[0:3].lower()
					return not(platUa == platFlash)
				else:
					platJs = self.platformJs[0:3].lower()
					return not(platUa == platJs)
			except:
				return True
		else:
			raise ValueError("Javascript is not activated")

	def hasFlashBlockedByExtension(self):
		return self.platformFlash == "Flash detected but blocked by an extension"

	##########

	#Methods to compare 2 Fingerprints :

	##########

	def hasSameOs(self, fp):
		return self.getOs() == fp.getOs()

	def hasSameBrowser(self, fp):
		return self.getBrowser() == fp.getBrowser()

	def hasSameTimezone(self, fp):
		return self.timezoneJs == fp.timezoneJs

	def hasSameResolution(self, fp):
		return self.resolutionJs == fp.resolutionJs

	def hasSameAdblock(self, fp):
		return self.adBlock == fp.adBlock

	def hasSameHttpLanguages(self, fp):
		return self.languageHttp == fp.languageHttp

	def hasSameAcceptHttp(self, fp):
		return self.acceptHttp == fp.acceptHttp

	def hasSameEncodingHttp(self, fp):
		return self.encodingHttp == fp.encodingHttp

	def hasSamePlugins(self, fp):
		return self.pluginsJs == fp.pluginsJs

	def hasSameFonts(self, fp):
		return self.fontsFlash == fp.fontsFlash

	def hasSamePlatformFlash(self, fp):
		return self.platformFlash == fp.platformFlash

	def hasSameResolutionFlash(self, fp):
		return self.resolutionFlash == fp.resolutionFlash

	def hasSameCanvasJsHashed(self, fp):
		return self.canvasJsHashed == fp.canvasJsHashed

	def hasSamePlatformJs(self, fp):
		return self.platformJs == fp.platformJs

	def hasSameAddressHttp(self, fp):
		return self.addressHttp == fp.addressHttp

	def hasSameDnt(self, fp):
		return self.dntJs == fp.dntJs

	def hasSameCookie(self, fp):
		return self.cookiesJs == fp.cookiesJs

	def hasSameLocal(self, fp):
		return self.localJs == fp.localJs

	def hasSameFlashBlocked(self, fp):
		return self.hasFlashBlockedByExtension() == fp.hasFlashBlockedByExtension()

	def hasSameLanguageInconsistency(self, fp):
		if self.languageInconsistency and fp.languageInconsistency:
			return "0"
		elif self.languageInconsistency or fp.languageInconsistency:
			return "1"
		else:
			return "2"

	def hasSamePlatformInconsistency(self, fp):
		if self.platformInconsistency and fp.platformInconsistency:
			return "0"
		elif self.platformInconsistency or fp.platformInconsistency:
			return "1"
		else:
			return "2"

	#Compare the current fingerprint with another one (fp)
	#Returns True if the current fingerprint has a highest (or equal) version of browser 
	def hasHighestBrowserVersion(self, fp):
		if self.counter > fp.counter:
			mostRecent = self
			oldest = fp
		else:
			mostRecent = fp
			oldest = self

		return mostRecent.browserVersion >= oldest.browserVersion
 

	#Returns True if the plugins of the current fingerprint are a subset of another fingerprint fp or the opposite
	#Else, it returns False
	def arePluginsSubset(self, fp):
		pluginsSet1 = set(self.getPlugins())
		pluginsSet2 = set(fp.getPlugins())
		return (pluginsSet1.issubset(pluginsSet2) or pluginsSet2.issubset(pluginsSet1))

	def getNumberDifferentPlugins(self, fp):
		pluginsSet1 = set(self.getPlugins())
		pluginsSet2 = set(fp.getPlugins())
		return max(self.getNumberOfPlugins(), fp.getNumberOfPlugins()) - len(pluginsSet1.intersection(pluginsSet2))

	#Returns True if the fonts of the current fingerprint are a subset of another fingerprint fp or the opposite
	#Else, it returns False
	def areFontsSubset(self, fp):
		fontsSet1 = set(self.getFonts())
		fontsSet2 = set(fp.getFonts())
		return (fontsSet1.issubset(fontsSet2) or fontsSet2.issubset(fontsSet1))

	#return True if 2 fingeprints belong to the same user (based on the id criteria)
	def belongToSameUser(self, fp):
		return self.id == fp.id
		
