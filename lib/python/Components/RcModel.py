import os

class RcModel:
	RCTYPE_DMM = 0
	RCTYPE_IOS100 = 1
	RCTYPE_IOS200 = 2
	RCTYPE_IOS300 = 3
	RCTYPE_TMTWIN = 4
	RCTYPE_TM2T = 5
	RCTYPE_TMSINGLE = 6
	RCTYPE_TMNANO = 7

	def __init__(self):
		self.currentRcType = self.RCTYPE_DMM
		self.readRcTypeFromProc()

	def rcIsDefault(self):
		if self.currentRcType != self.RCTYPE_DMM:
			return False
		return True

	def readFile(self, target):
		fp = open(target, 'r')
		out = fp.read()
		fp.close()
		return out.split()[0]
#[iq
	def readRcTypeFromProc(self):
		if os.path.exists('/proc/stb/info/hwmodel'):
			model = self.readFile('/proc/stb/info/hwmodel')
			if model == "tmtwinoe":
				self.currentRcType = self.RCTYPE_TMTWIN
			elif model == "ios100hd":
				self.currentRcType = self.RCTYPE_IOS100
			elif model == "ios200hd":
				self.currentRcType = self.RCTYPE_IOS200
			elif model == "ios300hd":
				self.currentRcType = self.RCTYPE_IOS300
			elif model == "tm2toe":
				self.currentRcType = self.RCTYPE_TM2T
			elif model == "tmsingle":
				self.currentRcType = self.RCTYPE_TMSINGLE
			elif model == "tmnanooe":
				self.currentRcType = self.RCTYPE_TMNANO

		elif os.path.exists('/proc/stb/info/boxtype'):
			model = self.readFile('/proc/stb/info/boxtype')
			if model.startswith('et') or model.startswith('xp'):
				rc = self.readFile('/proc/stb/ir/rc/type')
				if rc == '4':
					self.currentRcType = self.RCTYPE_DMM
				elif rc == '6':
					self.currentRcType = self.RCTYPE_DMM

	def getRcLocation(self):
		if self.currentRcType == self.RCTYPE_TMTWIN:
			return '/usr/share/enigma2/rc_models/tm/tmtwinoe/'
		elif self.currentRcType == self.RCTYPE_IOS100:
			return '/usr/share/enigma2/rc_models/tm/ios100/'
		elif self.currentRcType == self.RCTYPE_IOS200:
			return '/usr/share/enigma2/rc_models/tm/ios200/'
		elif self.currentRcType == self.RCTYPE_IOS300:
			return '/usr/share/enigma2/rc_models/tm/ios300/'
		elif self.currentRcType == self.RCTYPE_TM2T:
			return '/usr/share/enigma2/rc_models/tm/tm2toe/'
		elif self.currentRcType == self.RCTYPE_TMSINGLE:
			return '/usr/share/enigma2/rc_models/tm/tmsingle/'
		elif self.currentRcType == self.RCTYPE_TMNANO:
			return '/usr/share/enigma2/rc_models/tm/tmnanooe/'

rc_model = RcModel()
