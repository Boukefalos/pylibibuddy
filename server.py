#!/usr/bin/python

import logging
import sys
import socket
import pwd
import os
import time
from ConfigParser import RawConfigParser
from plibbuddy import BuddyDevice

#########################################
# Decoding macros
##########################################

def macro_color (red, green, blue):
    message = 'C:%d:%d:%d' % (red, green, blue)
    message += "\nX\nS\nZ\nZ\n"
    return message

def macro_heart ():
    message = 'H:1' 
    message += "\nX\nS\nZ\nZ\n"
    return message

def macro_move_flap():
    message  = "ML\nX\nS\nS\n"
    message += "MR\nX\nS\nS\n"
    message += "ML\nX\nS\nS\n"
    return message + macro_flap()

def macro_flap (heart=0):
    message = ''
    for i in range(2):
        message += "L\n"
        message += "WU\n"
        if heart:
            message += "H:1\n"
        message += "X\nS\nL\n"
        message += "WD\nX\nS\n"
    return message

def macro_heart2():
    message = "H:1\nX\nS\n"
    message += "Z\nS\n"
    message += "H:1\nX\nS\n"
    message += "Z\nS\n\nZ\nZ\n"
    return message

def macro_demo(num = 1):
    message = ''
    for i in range(num):
        message += "C:1:0:0\nH:0\nML\nWD\nX\nS\nS\n"
        message += "C:0:1:0\nH:1\nMR\nWU\nX\nS\nS\n"
        message += "C:0:0:1\nH:0\nML\nWD\nX\nS\nS\n"
        message += "C:1:0:1\nH:1\nMR\nWU\nX\nS\nS\n"
        message += "C:1:1:0\nH:0\nML\nWD\nX\nS\nS\n"
        message += "C:0:1:1\nH:1\nMR\nWU\nX\nS\nS\n"
        message += "C:1:1:1\nH:0\nML\nWD\nX\nS\nS\n"
        message += "Z\nZ\n"
    return message

def do_color(buddy, red, green, blue):
    r, g, b = buddy.getColors()
    try:
         param1 = int(red)
         param2 = int(green)
         param3 = int(blue)
    except:
         param1 = -1
         param2 = -1
         param3 = -1
    if (param1 == -1):
        param1 = r
    if (param2 == -1):
        param2 = g
    if (param3 == -1):
        param3 = b
    buddy.setHeadColors(param1, param2, param3)
    buddy.doCmd(0.5)

def decode_buddy(buddy, msg):
    orders = msg.split("\n") 
    for str in (orders): 
        cod = str.split(':')
        param = 0
        if cod[0] == 'RED' or cod[0] == 'R':
            try: do_color(buddy, cod[1], -1, -1)
            except: pass
        elif cod[0] == 'GREEN' or cod[0] == 'G':
            try: do_color(buddy,-1, cod[1], -1)
            except: pass
        elif cod[0] == 'BLUE' or cod[0] == 'B':
            try: do_color(buddy, -1, -1, cod[1])
            except: pass
        elif cod[0] == 'YELLOW':
            try: do_color(buddy, cod[1], cod[1], -1)
            except: pass
            continue
        elif cod[0] == 'SAPHIRE':
            try: do_color(buddy, -1, cod[1], cod[1])
            except: pass
        elif cod[0] == 'VIOLET':
            try: do_color(buddy, cod[1], -1, cod[1])
            except: pass
        elif cod[0] == 'HEART' or cod[0] == 'H':
            try:
                param = int(cod[1])
            except:
                param = 0
            buddy.setHeart(param)
        elif cod[0] == 'C':
            try: do_color(buddy, cod[1], cod[2], cod[3])
            except: pass
        elif cod[0] == 'MR':
            buddy.flick(buddy.RIGHT)
            continue
        elif cod[0] == 'ML':
            buddy.flick(buddy.LEFT)
        elif cod[0] == 'SLEEP' or cod[0] == 'S':
            time.sleep(0.1)
        elif cod[0] == 'WU':
            buddy.wing(buddy.UP)
        elif cod[0] == 'WD':
            buddy.wing(buddy.DOWN)
        elif cod[0] == 'EXEC' or cod[0] == 'X':
            buddy.pumpMessage()
        elif cod[0] == 'CLEAR' or cod[0] == 'L':
            buddy.resetMessage()
        elif cod[0] ==  'RESET' or cod[0] == 'Z':
            buddy.resetMessage()
            buddy.pumpMessage()
        elif cod[0] == 'MACRO_FLAP':
            decode_buddy(buddy, macro_move_flap())
        elif cod[0] == 'MACRO_FLAP2':
            decode_buddy(buddy, macro_flap())
        elif cod[0] == 'MACRO_RED':
            decode_buddy(buddy, macro_color(1, 0, 0))
        elif cod[0] == 'MACRO_GREEN':
            decode_buddy(buddy, macro_color(0, 1, 0))
        elif cod[0] == 'MACRO_BLUE':
            decode_buddy(buddy, macro_color(0,0,1))
        elif cod[0] == 'MACRO_YELLOW':
            decode_buddy(buddy, macro_color(1,1,0))
        elif cod[0] == 'MACRO_VIOLET':
            decode_buddy(buddy, macro_color(1,0,1))
        elif cod[0] == 'MACRO_SAPHIRE':
            decode_buddy(buddy, macro_color(0,1,1))
        elif cod[0] == 'MACRO_LBLUE':
            decode_buddy(buddy, macro_color(1,1,1))
        elif cod[0] == 'MACRO_HEART':
            decode_buddy(buddy, macro_heart())
        elif cod[0] == 'MACRO_HEART2':
            decode_buddy(buddy, macro_heart2())
        elif cod[0] == 'DEMO':
            decode_buddy(buddy, macro_demo())

#######################################
# MAIN program
#######################################

# Default config
config = RawConfigParser(
    { 'port': 8888,
      'address': '0.0.0.0',
      'deamon': False,
      'user': 'nobody',
      'loglevel': 'info',
      'logfile': 'console',
      'usbproduct': 0001,
     }
)
config._sections = {'network':{}, 'system':{}}
config_files = [ 'pybuddy.cfg',
                 '~/.pybuddy.cfg', 
                 '/etc/pybuddy/pybuddy.cfg', 
                 '/usr/local/etc/pybuddy.cfg']

# Parse config
if len(sys.argv) > 1:
    config_files.append(sys.argv[1])
    
config_read = config.read(config_files)

if config.get('system', 'logfile') != 'console':
    logging.basicConfig(
        filename = config.get('system', 'logfile'),
        format = '%(asctime)s %(levelname)-8s %(message)s',
    )
else:
    logging.basicConfig(
        stream = sys.stderr,
        format = '%(asctime)s %(levelname)-8s %(message)s'
    )

log = logging.getLogger('pybuddy')
if config.get('system', 'loglevel') == 'debug':
    log.setLevel(logging.DEBUG)
elif config.get('system', 'loglevel') == 'info':
    log.setLevel(logging.INFO)

if config_read:
    log.info('Read config file: %s', config_read[0])
    
# Initialize device
log.info('Starting search...')
try:
    buddy = BuddyDevice(0, int(config.get("system", "usbproduct")))
except NoBuddyException, e:
    log.error('Not found!')
    sys.exit(1)

if config.get('system', 'daemon') == True:
    # Daemonize
    log.info('Starting daemon...')
    if os.fork() == 0:
        os.setsid()
    else:
        sys.exit(0)

# Create server socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((config.get('network', 'address'), int(config.get('network', 'port'))))

# Drop privileges
try:
    uid = pwd.getpwnam(config.get('system', 'user'))[2]
except KeyError:
    log.error('Username %s not found, exiting...', config.get('system', 'user'))
    sys.exit(1)
os.setuid(uid)

# Main message loop
while 1:
    try:
        message, address = s.recvfrom(8192)
        log.debug('Got data from %s', address)
        decode_buddy(buddy, message)
    except (KeyboardInterrupt, SystemExit):
        raise