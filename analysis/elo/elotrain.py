#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 21:06:27 2020

@author: chris
"""

T2 = 1500
T1 = 1500
HGA = 20

exp = (1 / (1 + 10 ** ((T2 - T1 - HGA) / 400)))

print(exp)

old = 1500
k_factor = 40
score = 1


print(old + (k_factor * (score - exp)))

1500 + (40 * .10)