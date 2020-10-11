#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.main import main
from data.countingfingers import dedoscamp
import cProfile
import os
import threading


if __name__=='__main__':
    ThreadMain = threading.Thread(target=dedoscamp)
    ThreadMain.start()
    main()
    
    pg.quit()
    sys.exit()

    