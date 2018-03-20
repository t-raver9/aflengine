#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:47:24 2018

@author: chrisstrods
"""

def getPoints(df):
    return int(df["hteam_q4"].split(".")[2]) + \
            int(df["ateam_q4"].split(".")[2])