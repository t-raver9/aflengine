#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:51:02 2017

@author: chrisstrods
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:28:29 2017

@author: chrisstrods
"""

from lxml import html
from datetime import datetime
import functions as f
import beautifulsoup as bs


#used to store the lists
#playermatch = []
#quarters = []
#mdetails = []
#matchstats = []
#brownlow = []

url ='http://afltables.com/afl/stats/games/2017/031420170323.html'
tree = html.parse(url)

stats_match = tree.xpath('/html/body/center/table[1]/descendant::*/text()')
stats_home = tree.xpath('/html/body/center/table[3]/descendant::*/text()')
stats_away = tree.xpath('/html/body/center/table[5]/descendant::*/text()')
details_home = tree.xpath('/html/body/center/table[6]/descendant::*/text()')
details_away = tree.xpath('/html/body/center/table[7]/descendant::*/text()')
score_progression = tree.xpath('/html/body/center/table[8]/descendant::*/text()')

print(stats_match)
print(stats_home)
print(stats_away)
print(details_home)
print(details_away)
print(score_progression)