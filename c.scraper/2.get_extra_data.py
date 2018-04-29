#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:15:51 2018

@author: chrisstrods
"""

<<<<<<< HEAD
import pandas as pd
from lxml import html
from datetime import datetime
import functions as f
import re
from os.path import dirname, abspath
import os
=======
import numpy, pandas as pd
from lxml import html
from datetime import datetime
import requests
import functions as f
import re








#player_stats["fullname"] = player_stats["first_name"] + " " +  \
#    player_stats["last_name"]
        

#player_stats_test = player_stats.head(100)
#extra_players_test = extra_player_stats.head(100)
#extra_summaries_test = extra_summaries.head(n=100)

#

#extra_players_joined = pd.merge(extra_player_stats,extra_summaries,how="left",on="gameID")
#extra_players_joined_trimmed = extra_players_joined[['name','homeAway','hometeam','awayteam','AFLfantasy','Supercoach','matchid']]
#extra_players_joined_trimmed_test = extra_players_joined_trimmed.head(100)




#extra_players_joined_trimmed_test["Fuzzy1"] = extra_players_joined_trimmed_test.apply(fuzzy_match,
#                                args=(player_stats,fuzz.ratio, 80),axis=0)


#fantasy_joined["playermatchid"] = fantasy_joined.apply(getPlayerMatchID, axis=1)


#fantasy_test = fantasy_joined.head(n=100)


#fantasy_joined.to_csv("../extra_data/fantasy_joined.csv",mode="w")



#summaries_joined = pd.merge(summaries,extra_summaries,how="left",on="matchid")
#players_joined = pd.merge(player_stats,fantasy_joined,how="left",on="playermatchid")


#fantasy_test = fantasy_joined.head(n=100)
#summaries_test = summaries_joined.head(n=100)
#players_test = players_joined.head(n=100)


#players_joined.to_csv("../extra_data/players_joined.csv",mode="w")


#fantasy_joined["matchid"] = fantasy_joined.apply(getMatchID,axis=1)



>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85



#used to store the lists
playermatch = []
mdetails = []


<<<<<<< HEAD
daterange = [9514,9563]

#4961 - Round one 2010
#9513 - 2017 GF
#9558 - end round 5 2018
=======
daterange = [4961,9513]

#4961 - Round one 2010
#9531 - 2017 GF
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85




def loadData(gamerange):
    errorcount = 0
<<<<<<< HEAD
    d = dirname(dirname(abspath(__file__)))
=======
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
    for t in range(gamerange[0],gamerange[1]+1):
        if(t>9297 or t<6370):
            try:
                print("Processing game #" + str(t))
                #download file from server
<<<<<<< HEAD
                
                #url ='http://www.footywire.com/afl/footy/ft_match_statistics?mid=' + str(t)
                file = open(d + "/d.extrafiles/" + str(t) + ".html")
                #tree = etree.parse(response)
                tree = html.fromstring(file.read())
=======
                url ='http://www.footywire.com/afl/footy/ft_match_statistics?mid=' + str(t)
                response = requests.get(url)
                tree = html.fromstring(response.text)
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
                #print(page.read())
        

                #strip overall result and remove linebreaks                                                                 
                text_result = tree.xpath('//td[@class="hltitle"]/text()')
                text_result[0] = text_result[0].replace('\n','')

                
                #strip match details and remove linebreaks
                text_details = tree.xpath('//td[@class="lnorm"]/text()')
                for s in text_details:
                    s = s.replace('\n','')
                    
                
                #strip home team data from statbox and remove linebreaks
                year = int(text_details[1].split(" ")[3].replace(",",""))
                if(year < 2010):
                    player_stats_h = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[3]/td/table/tr[3]/td/table/tr[1]/td[1]/descendant::*/text()');
                else:
                    player_stats_h = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[1]/td[1]/descendant::*/text()');
                    
                for s in player_stats_h:
                    s = s.replace('\n','')

                                              

                #strip away team data from statbox and remove linebreaks    
                if(year < 2010):
                    player_stats_a = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[3]/td/table/tr[3]/td/table/tr/td/table/tr/td[1]/table/tr[3]/td/table/descendant::*/text()');                              
                else:
                    player_stats_a = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[3]/td[1]/descendant::*/text()');
                for s in player_stats_a:
                    s = s.replace('\n','')


                
                scrapeBasicStats(player_stats_h,str(t),playermatch, "Home", year)

                scrapeBasicStats(player_stats_a,str(t),playermatch, "Away", year)

                scrapeMatchDetails(str(text_details),str(text_result),str(t),mdetails)
                print("Successfully processed game #" + str(t))
            except IndexError:
                print("There was an index error with match #" + str(t))
                errorcount += 1 
        else:
            print("Skipping game #" + str(t))
            continue
        
    print("There were " + str(errorcount) + " number of games that failed")    
    return [playermatch,mdetails]



def scrapeBasicStats(gameIn,gameID,gameOut, homeAway,year):
    if(year < 2007 and homeAway == "Home"):
        i=26
    elif(year < 2007 and homeAway == "Away"):
        i=19
    else:
        i=21
        
    #print(gameIn)
    for x in range(0,22):
        if(year < 2007):
            i = i + 24
        else:
            i = i + 38
                         
        
        name = re.sub(r'[^\w\s]','',str(gameIn[i].encode('utf-8'))[2:-1])
<<<<<<< HEAD
        disp = int(gameIn[i+6].encode('utf-8'))

        if(year<2007):
            AFLfantasy = ""
            Supercoach = ""
            continue            
        else:
            AFLfantasy = int(gameIn[i+32].encode('utf-8'))
            Supercoach = int(gameIn[i+34].encode('utf-8'))
=======
        #kicks = int(gameIn[i+2].encode('utf-8'))
        #hb = int(gameIn[i+4].encode('utf-8'))
        disp = int(gameIn[i+6].encode('utf-8'))
        #marks = int(gameIn[i+8].encode('utf-8'))
        #goals = int(gameIn[i+10].encode('utf-8'))
        #behinds = int(gameIn[i+12].encode('utf-8'))
        #tackles = int(gameIn[i+14].encode('utf-8'))

        if(year<2007):
            #i50s = -1
        
            #hitouts = int(gameIn[i+16].encode('utf-8'))
            #freesFor = int(gameIn[i+18].encode('utf-8'))
            #freesAgainst = int(gameIn[i+20].encode('utf-8'))

            AFLfantasy = ""
            Supercoach = ""
            continue
            
        else:
            #i50s = int(gameIn[i+18].encode('utf-8'))
            #freesFor = int(gameIn[i+20].encode('utf-8'))
            #freesAgainst = int(gameIn[i+22].encode('utf-8'))
            AFLfantasy = int(gameIn[i+32].encode('utf-8'))
            Supercoach = int(gameIn[i+34].encode('utf-8'))
            #hitouts = int(gameIn[i+16].encode('utf-8'))
        
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
        
        gameOut.append({'gameID':gameID, 'homeAway':homeAway, 
                        'name':name, 'disposals':disp, 'AFLfantasy':AFLfantasy, 
                        'Supercoach':Supercoach})

    
def scrapeMatchDetails(gameIn,gameResult,gameID,gameOut):
    gameString = gameIn.replace('\\n','').replace("'",'').split(',')
    mround = gameString[0].split(' ')[1]
    if(not(int(gameID) < 1840)):
<<<<<<< HEAD
        date = datetime.strptime(f.changeDate(gameString[4]),'%d %B %Y').date()
        time = str(gameString[5].split(" ")[1] + gameString[5].split(" ")[2] )

=======
        #venue = "N/A"
        #crowd = "N/A"
        #date = "N/A"
        #time = "N/A"
        #day = "N/A"
        date = datetime.strptime(f.changeDate(gameString[4]),'%d %B %Y').date()
        time = str(gameString[5].split(" ")[1] + gameString[5].split(" ")[2] )
    #else:
        #venue = gameString[1]
        #crowd = gameString[2].split(' ')[2]
        #day = gameString[3]
        #print(gameString)
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85
    
    #odds only collected since 2010, and footywire is missing 2017 GF odds
    if(date.year > 2009 and not(int(gameID) == 9513)): 
        if "Brownlow" not in str(gameString):
            homeodds = gameString[6].split(":")[1].split(" ")[2]
            homeline = gameString[7].split("@")[0].split(" ")[2]
            awayodds = gameString[8].split(":")[1].split(" ")[2]
            awayline = gameString[9].split("@")[0].split(" ")[2]
        else:
            homeodds = -1
            homeline = -1
            awayodds = -1
            awayline = -1
    else:
        homeodds = -1
        homeline = -1
        awayodds = -1
        awayline = -1
    
    resultsString = gameResult.replace("'","").replace("defeats","defeated by").replace("defeat ","defeated by").replace("[","").replace("]","").replace("drew with","defeated by")
    results = resultsString.split("defeated by")
    home = results[0]
    away = results[1]
    
    
    
    gameOut.append({'gameID':gameID, 'round':mround.strip(), 'date':str(date), 'time':time, 'homeodds':float(homeodds),
                    'homeline':float(homeline), 'awayodds':float(awayodds), 'awayline':float(awayline),
                    'hometeam':home.strip(), 'awayteam':away.strip()})

    
    
    
data = loadData(daterange)

#playerstats = data[0]
#matchdetails = data[1]

<<<<<<< HEAD
if(os.path.isfile("../d.input/fantasy_scores.csv")):
    pd.DataFrame.from_dict(playermatch).to_csv("../d.input/fantasy_scores.csv", mode="a", index = False, header=False)
else:
    pd.DataFrame.from_dict(playermatch).to_csv("../d.input/fantasy_scores.csv", mode="w", index = False)
    
if(os.path.isfile("../d.input/odds_data.csv")):
    pd.DataFrame.from_dict(mdetails).to_csv("../d.input/odds_data.csv", mode="a", index = False, header=False)
else:
    pd.DataFrame.from_dict(mdetails).to_csv("../d.input/odds_data.csv", mode="w", index = False)



=======
pd.DataFrame.from_dict(playermatch).to_csv("../d.input/fantasy_scores.csv", mode="w")
pd.DataFrame.from_dict(mdetails).to_csv("../d.input/odds_data.csv", mode="w")
>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85

