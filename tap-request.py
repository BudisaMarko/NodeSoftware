#!/usr/bin/env python

from tap import *

class MyThread ( threading.Thread ):
    def run ( self ):
        tap=TAP()
        tap.run()
#        print tap


if __name__=='__main__': 
    for i in xrange(10):
        MyThread().start()

