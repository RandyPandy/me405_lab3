##
#Part of code sourced from 'Python - read from the serial port data line by line into a list when available'
#stackoverflow.com
#Author: Mitchell Chu
#
#

import serial
import time



class Serial_Port:
    def __init__(self):
        self.wr_tout = 2
        self.path = '/dev/ttyACM0'
        self.tout = 2 ##2s timeout
        self.baud = 115200

    def read_list(self, command):
        data = []
        with serial.Serial(path, self.baud, timeout=self.tout, write_timeout=self.wr_tout) as ser_port:
        if ser_port.is_open:
            ser_port.write(b+command)
            while True:
                size = ser_port.inWaiting()
                if size:
                    line = ser_port.read(size)
                    data.append(line)
                    ##line = ser_port.readline()
                    print line
                else:
                    print 'no data'
                time.sleep(1)
            ser_port.close
        else:
            print 'ser_port not open'
        return data
        

    def set_baud(self,baud):
        self.baud = baud

    def set_wr_tout(self, wr_tout):
        self.tout = wr_tout

    def set_path(self, path):
        self.path = path

    def set_tout(self, tout):
        self.tout= tout
