#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 21:29:50 2017

@author: chrisstrods
"""
      
    
def changeDate(date):
    dstring = date.split(' ')
    newdate = str(dstring[1].strip('stndrh') + " " + dstring[2] + " " + dstring[3])
    return newdate
