from Screen import Screen
from Components.ChoiceList import ChoiceEntryComponent, ChoiceList
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Label import MultiColorLabel
from Components.config import ConfigIP, NoSave
from Components.Network import iNetwork
from Components.Console import Console
from enigma import eTimer
import os, fcntl, array

class TestMenu(Screen):
	skin = """
        <screen name="TestMenu" position="fill" title="Test Menu" flags="wfNoBorder">
			<eLabel position="fill" backgroundColor="transpBlack" zPosition="-50"/>
			<widget name="menulist" position="60,75" scrollbarMode="showNever" size="400,400" zPosition="2" font="Regular; 22" foregroundColor="white" backgroundColor="transpBlack" transparent="1"/>
			<widget name="lan" position="460,185" size="250,30" foregroundColors="transpBlack,red,green" backgroundColors="transpBlack,red,green" zPosition="1" foregroundColor="white" font="Regular;22" />
			<widget name="sc0" position="460,220" size="250,30" foregroundColors="transpBlack,red,green" backgroundColors="transpBlack,red,green" zPosition="1" foregroundColor="white" font="Regular;22" />
			<widget name="sc1" position="460,245" size="250,30" foregroundColors="transpBlack,red,green" backgroundColors="transpBlack,red,green" zPosition="1" foregroundColor="white" font="Regular;22" />
        </screen>"""

	CARD_LIST = {
		chr(0x3b) + chr(0x9f) + chr(0x21) + chr(0x0e) + chr(0x49) + chr(0x52) + chr(0x44) : "Irdeto",
		chr(0x3b) + chr(0xf7) + chr(0x11) + chr(0x00) : "Seca",
		chr(0x3b) + chr(0x78) + chr(0x12) : "Cryptoworks", 
		chr(0x3b) + chr(0x26) + chr(0x00) : "Conax", 
		chr(0x3b) + chr(0x24) + chr(0x00) : "Conax", 
		chr(0x3b) + chr(0x34) + chr(0xd6) : "Drecrypt", 
		chr(0x3f) + chr(0xff) + chr(0x95) : "Nagravision", 
		chr(0x3f) + chr(0x7f) + chr(0x13) : "NDS", 
		chr(0x3f) + chr(0xfd) + chr(0x13) : "NDS", 
		chr(0x3f) + chr(0x27) + chr(0x17) : "Viaccess", 
		chr(0x3f) + chr(0x77) + chr(0x18) : "Viaccess", 
		chr(0x3b) + chr(0x77) + chr(0x18) : "Viaccess", 
		chr(0x3b) + chr(0x9c) + chr(0x13) + chr(0x11) + chr(0x81) + chr(0x64) + chr(0x72) : "Firecrypt", 
		chr(0x3b) + chr(0xec) + chr(0x00) + chr(0x00) + chr(0x40) + chr(0x38) + chr(0x57) : "Type1", 
		chr(0x3b) + chr(0xff) + chr(0xe0) + chr(0x1c) + chr(0x57) + chr(0xe0) + chr(0x74) : "Type2",
		chr(0x3f) + chr(0xfd) + chr(0x95) + chr(0x00) + chr(0xff) + chr(0x91) + chr(0x81) : "Type3"} 

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session

		list = [(_("hello"), self.func), 
		(_("goodbye"), self.func),
		(_("die"), self.func),
		(_("alive"), self.func),
		(_("sun"), self.func),
		(_("moon"), self.func),
		(_("gun"), self.func),
		(_("song"), self.func),
		(_("light"), self.func),
		(_("flash"), self.func),
		(_("lanOff"), self.func),
		(_("lanOn"), self.func)]

		self.__keys = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "red", "green", "yellow", "blue" ] + (len(list) - 10) * [""]
		self.list = []

		pos = 0
		self.keymap = {}
		for x in list:
			strpos = str(self.__keys[pos])
			self.list.append(ChoiceEntryComponent(key = strpos, text = x))
			if self.__keys[pos] != "":
				self.keymap[self.__keys[pos]] = list[pos]
			pos += 1

		self["menulist"] = ChoiceList(self.list)
		self["menulist"].show()

		self["lan"] = MultiColorLabel(_(" IP : N/A"))
		self["lan"].setBackgroundColorNum(0)
		self["lan"].show()

		self["sc0"] = MultiColorLabel(_(" SC Slot0 : N/A"))
		self["sc0"].setBackgroundColorNum(0)
		self["sc0"].show()
#		self["sc1"] = MultiColorLabel(_(" SC Slot1 : N/A"))
#		self["sc1"].setBackgroundColorNum(0)
#		self["sc1"].show()

		self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions", "InfobarChannelSelection"], 
				{
				"ok": self.go,
				"back": self.cancel,
				"up": self.up,
				"down": self.down,
				"1": self.keyNumberGlobal,
				"2": self.keyNumberGlobal,
				"3": self.keyNumberGlobal,
				"4": self.keyNumberGlobal,
				"5": self.keyNumberGlobal,
				"6": self.keyNumberGlobal,
				"7": self.keyNumberGlobal,
				"8": self.keyNumberGlobal,
				"9": self.keyNumberGlobal,
				"0": self.keyNumberGlobal,
				"red": self.keyRed,
				"green": self.keyGreen,
				"yellow": self.keyYellow,
				"blue": self.keyBlue,
				}, -1)

		self.iface = "eth0"
		self.networkMonitor = eTimer()
		self.networkMonitor.callback.append(self.getLinkState)
		self.networkMonitor.start(1000, True)

		self.smartcardInserted = [ False, False ]
		self.smartcardConsole = Console()
		self.smartcardMonitor = eTimer()
		self.smartcardMonitor.callback.append(self.getSCState)
		self.smartcardMonitor.start(1000, False)

	def cancel(self):
		self.close()

	def keyLeft(self):
		pass
	
	def keyRight(self):
		pass
	
	def up(self):
		if len(self["menulist"].list) > 0:
			while 1:
				self["menulist"].instance.moveSelection(self["menulist"].instance.moveUp)
				if self["menulist"].l.getCurrentSelection()[0][0] != "--" or self["menulist"].l.getCurrentSelectionIndex() == 0:
					break

	def down(self):
		if len(self["menulist"].list) > 0:
			while 1:
				self["menulist"].instance.moveSelection(self["menulist"].instance.moveDown)
				if self["menulist"].l.getCurrentSelection()[0][0] != "--" or self["menulist"].l.getCurrentSelectionIndex() == len(self["menulist"].list) - 1:
					break

	# runs a number shortcut
	def keyNumberGlobal(self, number):
		self.goKey(str(number))

	# runs the current selected entry
	def go(self):
		cursel = self["menulist"].l.getCurrentSelection()
		if cursel:
			self.goEntry(cursel[0])
		else:
			self.cancel()

	# runs a specific entry
	def goEntry(self, entry):
		entry[1]()

	# lookups a key in the keymap, then runs it
	def goKey(self, key):
		if self.keymap.has_key(key):
			self["menulist"].instance.moveSelectionTo(self.__keys.index(key))
			entry = self.keymap[key]
			self.goEntry(entry)

	# runs a color shortcut
	def keyRed(self):
		self.goKey("red")

	def keyGreen(self):
		self.goKey("green")

	def keyYellow(self):
		self.goKey("yellow")

	def keyBlue(self):
		self.goKey("blue")

	def func(self):
		print self["menulist"].getCurrent()[0]

# ---------------------------------------------------------------------
#  lan check
# ---------------------------------------------------------------------
	def getLinkState(self):
		if iNetwork.isWirelessInterface(self.iface):
			try:
				from Plugins.SystemPlugins.WirelessLan.Wlan import iStatus
			except:
				self["lan"].setText(_(" IP : N/A"))
				self["lan"].setBackgroundColorNum(1)
			else:
				iStatus.getDataForInterface(self.iface, self.getInfoCB)
		else:
			iNetwork.getLinkState(self.iface, self.dataAvail)

	def dataAvail(self, data):
		self.LinkState = None
		for line in data.splitlines():
			line = line.strip()
			if 'Link detected:' in line:
				if "yes" in line:
					self.LinkState = True
				else:
					self.LinkState = False
		if self.LinkState == True:
			iNetwork.checkNetworkState(self.checkNetworkCB)
		else:
			self["lan"].setText(_(" IP : N/A"))
			self["lan"].setBackgroundColorNum(1)
			self.networkMonitor.start(1000, True)

	def getInfoCB(self,data,status):
		self.LinkState = None
		if data is not None:
			if data is True:
				if status is not None:
					if status[self.iface]["essid"] == "off" or status[self.iface]["accesspoint"] == "Not-Associated" or status[self.iface]["accesspoint"] == False:
						self.LinkState = False
						self["lan"].setText(_(" IP : N/A"))
						self["lan"].setBackgroundColorNum(1)
						self.networkMonitor.start(1000, True)
					else:
						self.LinkState = True
						iNetwork.checkNetworkState(self.checkNetworkCB)

	def checkNetworkCB(self,data):
		if iNetwork.getAdapterAttribute(self.iface, "up") is True:
			if self.LinkState is True:
				if data <= 2:
					self["lan"].setText(_(" IP : %s" % NoSave(ConfigIP(default=iNetwork.getAdapterAttribute(self.iface, "ip")) or [0,0,0,0]).getText()))
					self["lan"].setBackgroundColorNum(2)
				else:
					self["lan"].setText(_(" IP : N/A"))
					self["lan"].setBackgroundColorNum(1)
			else:
				self["lan"].setText(_(" IP : N/A"))
				self["lan"].setBackgroundColorNum(1)
		else:
			self["lan"].setText(_(" IP : N/A"))
			self["lan"].setBackgroundColorNum(1)
		self.networkMonitor.start(1000, True)

# ---------------------------------------------------------------------
#  smartcard check
# ---------------------------------------------------------------------
	def getSCInfo(self, index = 0):
		card = "N/A"
		device = open("/dev/sci%d" % index, "rw")
		try:
			fcntl.ioctl(device.fileno(), 0x80047301)
			atr = device.read()
			for atrHead in self.CARD_LIST.keys():
				if atr.startswith(atrHead):
					card = self.CARD_LIST[atrHead]
		except:
			card = "Unknown"
		return card

	def checkSCSlot(self, index = 0):
		inserted = array.array('h', [0])
		if os.path.exists("/dev/sci%d" % index):
			device = open("/dev/sci%d" % index, "rw")
			fcntl.ioctl(device.fileno(), 0x80047308, inserted, 1)
			device.close()
		return inserted[0]

	def getSCState(self):
		i = 0
		if self.checkSCSlot():
			if not self.smartcardInserted[i]:
				self["sc%d" % i].setText(_(" SC Slot%d : %s" % (i, self.getSCInfo(i))))
				self["sc%d" % i].setBackgroundColorNum(2)
			self.smartcardInserted[i] = True
		else:
			if self.smartcardInserted[i]:
				self["sc%d" % i].setText(_(" SC Slot%d : N/A" % i))
				self["sc%d" % i].setBackgroundColorNum(0)
			self.smartcardInserted[i] = False

