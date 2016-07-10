#!/usr/bin/python
import configparser
from time import sleep
from ibuddy import ibuddy, DeviceNotFoundException

if __name__ == '__main__':
    try:
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            product = int(config.get('system', 'product'))
        except:
            exit('[error] Failed to read config file!')
  
        ibuddy = ibuddy(product)
    except DeviceNotFoundException:
        print('No iBuddy device found!')
        exit(1)

    ibuddy.doColorName(ibuddy.PURPLE, 0.5)
    ibuddy.doColorName(ibuddy.BLUE, 0.5)
    ibuddy.doColorName(ibuddy.LTBLUE, 0.5)
    ibuddy.doColorName(ibuddy.YELLOW, 0.5)
    ibuddy.doColorName(ibuddy.GREEN, 0.5)
    ibuddy.doColorName(ibuddy.RED, 0.5)
    ibuddy.doColorName(ibuddy.WHITE, 0.5)
    ibuddy.doFlap()
    sleep(1)
    ibuddy.doWiggle() # does not work!
    sleep(1)
    ibuddy.doHeartbeat()
    sleep(1)
    ibuddy.doReset()