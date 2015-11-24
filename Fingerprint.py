from ua_parser import user_agent_parser
import re

class Fingerprint():

	def __init__(self, attributes):
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
		self.canvasJSHashed = attributes["canvasJSHashed"]
		self.localJs = attributes["localJS"]
		self.platformJs = attributes["platformJS"]
		self.userAgentInfo = dict()


	def hasJsActivated(self):
		return self.platformJs != "no JS"

	def hasFlashActivated(self):
		return self.fontsFlash != "Flash detected but not activated (click-to-play)" 

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
		if self.hasJsActivated():
			return len(re.findall("Plugin [0-9]+: ([a-zA-Z -.]+)", self.pluginsJs))
		else:
			raise ValueError("Javascript is not activated")

	def getMajorBrowserVersion(self):
		if len(self.userAgentInfo) == 0:
			self.userAgentInfo = user_agent_parser.Parse(self.userAgentHttp)
		return self.userAgentInfo["user_agent"]["major"]

	def getMinorBrowserVersion(self):
		if len(self.userAgentInfo) == 0:
			self.userAgentInfo = user_agent_parser.Parse(self.userAgentHttp)
		return self.userAgentInfo["user_agent"]["minor"]

	def getBrowser(self):
		if len(self.userAgentInfo) == 0:
			self.userAgentInfo = user_agent_parser.Parse(self.userAgentHttp)
		return self.userAgentInfo['user_agent']['family']

	def getOs(self):
		if len(self.userAgentInfo) == 0:
			self.userAgentInfo = user_agent_parser.Parse(self.userAgentHttp)
		return self.userAgentInfo["os"]["family"]

	##########

	#Methods to compare 2 Fingerprints :

	##########

	def hasSameOs(self, fp):
		return self.getOs() == fp.getOs()

	def hasSameBrowser(self, fp):
		return self.getBrowser() == fp.getBrowser

	#Compare the current fingerprint with another one (fp)
	#Returns True if the current fingerprint has a highest (or equal) version of browser 
	def hasHighestBrowserVersion(self, fp):
		if self.getMajorBrowserVersion() > fp.getMajorBrowserVersion():
			return True
		elif self.getMinorBrowserVersion() > fp.getMinorBrowserVersion():
			return True
		elif self.getMajorBrowserVersion() == fp.getMajorBrowserVersion() and \
			self.getMinorBrowserVersion() == fp.getMinorBrowserVersion():
			return True

		return False 

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

	#We compare the current fingerprint with another one (fp)
	#The goal is to determine if the current fp and the other belongs to the same user
	#Constraint : fp most be older than the current fp
	def belongsToSameUser(self, fp):
		#first we start by looking if the version is greater or equal
		if not self.hasHighestBrowserVersion(fp):
			return False

		
