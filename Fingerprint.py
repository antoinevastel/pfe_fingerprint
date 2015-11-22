
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


	def hasJsActivated(self):
		return self.platformJS != "no JS"

	def hasFlashActivated(self):
		return fontsFlash != "Flash detected but not activated (click-to-play)" 

	