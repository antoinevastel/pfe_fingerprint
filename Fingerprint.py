from ua_parser import user_agent_parser

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
		return self.platformJS != "no JS"

	def hasFlashActivated(self):
		return self.fontsFlash != "Flash detected but not activated (click-to-play)" 

	def getNumberFonts(self):
		if self.hasFlashActivated():
			return len(self.fontsFlash.split("_"))
		else:
			raise ValueError("Flash is not activated")

	def getNumberOfPlugins(self):
		if self.hasJsActivated():
			return len(re.findall("Plugin [0-9]+: ([a-zA-Z -.]+)", self.pluginsJs))
		else:
			raise ValueError("Javascript is not activated")

	def getBrowserVersion(self):
		if len(self.userAgentInfo) == 0:
			self.userAgentInfo = user_agent_parser.Parse(self.userAgentHttp)

		return self.userAgentInfo["user_agent"]["major"] + self.userAgentInfo["user_agent"]["minor"]

	def getOs(self):
		if len(self.userAgentInfo) == 0:
			self.userAgentInfo = user_agent_parser.Parse(self.userAgentHttp)

		return self.userAgentInfo["os"]["family"]
