#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:54:07 2018

@author: chrisstrods
"""

from bs4 import BeautifulSoup
import urllib, os, json, sys



#startyear - earliest year to get
#endyear - lastest year to get
def getPageNames(startyear, endyear):  #Gets JSON list of URLS
    base = 'https://afltables.com/afl/seas/'
    end = ".html"
    matchlist = dict()
    year = endyear

    #loops backwards from endyear to startyear
    while(year>=startyear):
        url = base + str(year) + end
        
        #get page containing all match links in the season
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        matches = list()

        #Get all links on the page
        for a in soup.findAll('a',href=True):
            
            #If link text is 'match stats' then it links to a game, so
            #record that URL in the list
            if(a.text=="Match stats"):
                matchstring = "https://afltables.com/afl/" + str(a['href'])[3:]
                matches.append(matchstring)
                matchlist.update({year:matches})
        print("Successfully downloaded match codes for " + str(year) + " season")
        year -= 1
        

    #When all seasons are done, output to JSON list
    with open('../matchfiles/matchlist.json','w') as fout:
        json.dump(matchlist,fout)

#Get files from JSON list and store them in the        
def getPages():
    #load list from JSON file
    with open('../matchfiles/matchlist.json','r') as fin:
        data = json.load(fin)
    
    #Iterate through each year in the list
    for year, mlist in data.items():
        print("Downloading " + str(year) + " season")
        #Create folder for that year if it doesn't exist
        if not os.path.exists("../matchfiles/" + year):
            os.makedirs("../matchfiles/" + year)
        #Iterate through each match in the year
        for matchurl in mlist:
            code = str(matchurl).rpartition('/')[2]
            urllib.request.urlretrieve(matchurl, 
                "../matchfiles/" + year + "/" + code)
        print("Successfully downloaded matches for " + str(year) + " season") 
            

    
#If run from command line, takes year ranges as parameters, otherwise
#uses defaults
if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Using default season range of 1897 to 2017")
        syear = 1897
        eyear = 2017
    else:
        syear = int(sys.argv[1])
        eyear = int(sys.argv[2])
    
    getPageNames(syear,eyear)
    getPages()

 