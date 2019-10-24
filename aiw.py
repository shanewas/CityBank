# -*- coding: utf-8 -*-
"""AIW Base Framework

-*- aiw.py -*-

This file is the starting point of the bots. The developer may think of it
as the trigger file. The Bot classes will be instantiated here and the onStart()
method will be called to start running the bots. 

Example:
    
    The rest of the code in this file can be considered as an example to follow,
    and discarded while coding        

Creators:
    Names: Ehfaz & Shane
    Date of last edit: 24/10/2019
"""
#Your code starts from here

# Imports

from src.bot1.bot import *

process = Bot("AIW test")
process.onStart()