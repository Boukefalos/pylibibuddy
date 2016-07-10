import usb
from time import sleep

class DeviceNotFoundException(Exception): pass

class ibuddy:
  USB_VENDOR  = 0x1130
  USB_PRODUCT = 0x0001
  SETUP         = (0x22, 0x09, 0x00, 0x02, 0x01, 0x00, 0x00, 0x00)
  MESS          = (0x55, 0x53, 0x42, 0x43, 0x00, 0x40, 0x02)

  WAITTIME = 0.1
  
  LEFT  = 0
  RIGHT = 1
  UP    = 0
  DOWN  = 1
  OFF   = 0
  ON    = 1

  BLUE   = (0,0,1)
  GREEN  = (0,1,0)
  LTBLUE = (0,1,1)
  PURPLE = (1,0,1)
  RED    = (1,0,0)
  WHITE  = (1,1,1)
  YELLOW = (1,1,0)

  CLEAR   = 0xFF
  finalMess = CLEAR
  command = CLEAR


  def __init__(self, product=None):
    if product is None:
          product = self.USB_PRODUCT
    busses = usb.busses()
    for bus in busses:
          for dev in bus.devices:
                if dev.idVendor == self.USB_VENDOR and dev.idProduct == product:
                    self.dev = dev
    if not hasattr(self, 'dev'):
          raise DeviceNotFoundException()
    self.handle = self.dev.open()

  def __send(self, inp):
    """ send your command to the device """
    try:
        self.handle.controlMsg(0x21, 0x09, self.SETUP, 0x02, 0x01)
        self.handle.controlMsg(0x21, 0x09, self.MESS+(inp,), 0x02, 0x01)
    except usb.USBError:
        self.__init__()

  def pumpMessage(self):
     self.send(self.finalMess)

  def resetMessage(self):
     self.finalMess = self.CLEAR

  def doCmd(self, seconds=WAITTIME):
    """ send the command specified by the current command """
    self.__send(self.command)
    sleep(seconds)

  def resetCmd(self):
    """ reset command to default (must pump to take effect) """
    self.command = self.CLEAR

  def setReverseBitValue(self,num,value):
    """ commands are sent as disabled bits """
    if (value==1):
        temp = 0xFF - (1<<num)
        self.command = self.command & temp
    elif (value==0):
        temp = 1 << num
        self.command = self.command | temp

  def getReverseBitValue(self,num):
    """ what was that bit set to again? """  
    temp = self.command
    temp = temp >> num
    res = not(temp&1)
    return res

  def setHeart(self, status):
    """ heart-light can be on (1) or off (0) """  
    self.setReverseBitValue(7, status)

  def flick(self, direction):
     if (direction == self.RIGHT):
          self.setReverseBitValue(1,1)
          self.setReverseBitValue(0,0)
     elif(direction == self.LEFT):
          self.setReverseBitValue(1,0)
          self.setReverseBitValue(0,1)

  def wing(self, direction):
     if (direction == self.UP):
          self.setReverseBitValue(3,1)
          self.setReverseBitValue(2,0)
     elif(direction == self.DOWN):
          self.setReverseBitValue(3,0)
          self.setReverseBitValue(2,1)

  def getColors (self):
     return self.getReverseBitValue(4), self.getReverseBitValue(5), self.getReverseBitValue(6)

  def getHeart(self):
     """ returns heart-light status of on (1) or off (0) """
     return self.getReverseBitValue(7)

  def getWing(self):
     """ returns wing status of BuddyDevice.UP (0) or BuddyDevice.DOWN (1) """
     return self.getReverseBitValue(2)

  def getDirection(self):
     return self.getReverseBitValue(1)

  def send(self, inp):
    try:
          self.dev.handle.controlMsg(0x21, 0x09, self.SETUP, 0x02, 0x01)
          self.dev.handle.controlMsg(0x21, 0x09, self.MESS+(inp,), 0x02, 0x01)
    except usb.USBError:
          self.__init__(self.battery, self.product)

  def setHeadColors(self, red, green, blue):
    """ colors as (red, green, blue) can be on (1) or off (0) """
    self.setReverseBitValue(4, red)
    self.setReverseBitValue(5, green)
    self.setReverseBitValue(6, blue)

  def getHeadColors(self):
    """ returns color status as tuple representing (red, green, blue) as on (1) or off (0) """
    return self.getReverseBitValue(4), self.getReverseBitValue(5), self.getReverseBitValue(6)

  def setHeart(self, status):
    """ heart-light can be on (1) or off (0) """
    self.setReverseBitValue(7,status)

  def getHeart(self):
    """ returns heart-light status of on (1) or off (0) """
    return self.getReverseBitValue(7)

  def setWing(self, direction):
    """ move the wings BuddyDevice.UP (0) or BuddyDevice.DOWN (1) """
    if (direction == self.UP):
        self.setReverseBitValue(3,1)
        self.setReverseBitValue(2,0)
    elif(direction == self.DOWN):
        self.setReverseBitValue(3,0)
        self.setReverseBitValue(2,1)

  def getWing(self):
    """ returns wing status of BuddyDevice.UP (0) or BuddyDevice.DOWN (1) """
    return self.getReverseBitValue(2)

  def setSwivel(self, direction):
    """ swivel the body BuddyDevice.LEFT (0) or BuddyDevice.RIGHT (1) """
    if (direction == self.RIGHT):
        self.setReverseBitValue(1,1)
        self.setReverseBitValue(0,0)
    elif(direction == self.LEFT):
        self.setReverseBitValue(1,0)
        self.setReverseBitValue(0,1)

  def getSwivel(self):
    """ returns current swivel direction as BuddyDevice.LEFT (0) or BuddyDevice.RIGHT (1) """
    return self.getReverseBitValue(1)

  def doReset(self, seconds=WAITTIME):
    """ reset to default positions/off, run command immediately """
    self.resetCmd()
    self.doCmd(seconds)

  def doFlap(self, times=3, seconds=0.2):
    """ flap wings X times with Y seconds pause in between, run command immediately """
    for i in range(times):
        self.setWing(self.UP)
        self.doCmd(seconds)
        self.setWing(self.DOWN)
        self.doCmd(seconds)

  def doWiggle(self, times=3, seconds=0.2):
    """ wiggle back and forth X times with Y seconds pauses, run command immediately """
    for i in range(times):
        self.setSwivel(self.LEFT)
        self.doCmd(seconds)
        self.setSwivel(self.RIGHT)
        self.doCmd(seconds)

  def doHeartbeat(self, times=3, seconds=0.3):
    """ blink heart X times with Y seconds' pause in betwee, run command immediately """
    for i in range(times):
        self.setHeart(self.ON)
        self.doCmd(seconds)
        self.setHeart(self.OFF)
        self.doCmd(seconds)

  def doColorRGB(self, r, g, b, seconds=WAITTIME):
    """ set head color by red/green/blue values 0 or 1, run command immediately """
    self.setHeadColors(r, g, b)
    self.doCmd(seconds)

  def doColorName(self, rgb, seconds=WAITTIME):
    """ set head color with color name tuples, run command immediately """
    self.setHeadColors(*rgb)
    self.doCmd(seconds)