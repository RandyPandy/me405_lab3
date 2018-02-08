#!/usr/bin/env python3
__author__ = "Matthew Ng"
__date__ = "1/17/18"
from matplotlib import pyplot as plt

class ericreader():
    def __init__(self):
        self.lines = []
        self.lines_x = []
        self.lines_y = []

    def int_or_float(self,s):
        '''
        Function from John Machin on stackoverflow
        https://stackoverflow.com/questions/5608702/how-can-i-convert-a-string-to-either-int-or-float-with-priority-on-int
        @param s string that is either a float or int
        @return the number in float or int form depending on what it is
        '''
        try:
            return int(s)
        except ValueError:
            return float(s)

    def is_number(self,s):
        ''' Function from Daniel Goldberg on stackoverflow https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
        @param s string to determine if that string is a number
        @return T/F depending on if that string is a number
        '''
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def clear_vars(self):
        self.lines = []
        self.lines_x = []
        self.lines_y = []
    
    def ericread(self):
        self.lines = []
        with open("eric.csv") as file:
            self.lines = [line.partition('#')[0].rstrip() for line in file]# Removes comments
            self.lines = [line.split(",")[:2] for line in self.lines] #splits up string and returns first 2 elem
            self.lines = [[x.strip() for x in line] for line in self.lines if len(line) > 1] #removes less than 2 elem
            plt.xlabel(self.lines[0][0]) #x label on plot
            plt.ylabel(self.lines[0][1]) #y label on plot
            self.lines = [x for x in self.lines if self.is_number(x[0]) and self.is_number(x[1])] #keeps if both elem are #'s

            #splitting up the list into X and Y
            self.lines_x = [self.int_or_float(line[0]) for line in self.lines[1:]]
            self.lines_y = [self.int_or_float(line[1]) for line in self.lines[1:]]

            plt.title('Homework 1 - Matthew Ng') #title
            plt.plot(self.lines_x, self.lines_y) #plot values
            plt.show() #show graph
