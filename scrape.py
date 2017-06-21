#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:28:29 2017

@author: chrisstrods
"""

from lxml import html
from datetime import datetime
import functions as f

#used to store the lists
playermatch = []
quarters = []
mdetails = []
matchstats = []
brownlow = []

def loadData(gamerange):
    errorcount = 0
    for t in range(gamerange[0],gamerange[1]+1):
        if(t>9297 or t<6370):
            try:
                print("Processing game #" + str(t))
                #download file from server
                url ='http://www.footywire.com/afl/footy/ft_match_statistics?mid=' + str(t)    
                tree = html.parse(url)
        
                #strip overall result and remove linebreaks                                                                 
                text_result = tree.xpath('//td[@class="hltitle"]/text()')
                text_result[0] = text_result[0].replace('\n','')

                #strip match details and remove linebreaks
                text_details = tree.xpath('//td[@class="lnorm"]/text()')
                for s in text_details:
                    s = s.replace('\n','')
            
                #strip match details and remove linebreaks
                bvotes = tree.xpath('//td[@class="lnorm"]/descendant::*/text()')
                for s in text_details:
                    s = s.replace('\n','')             
    
                #strip quarter breakdown and remove linebreaks
                text_quarters = tree.xpath('//table[@id="matchscoretable"]/descendant::*/text()');
                for s in text_quarters:
                    s = s.replace('\n','')

                #strip home team data from statbox and remove linebreaks
                player_stats_h = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[1]/td[1]/descendant::*/text()');
                for s in player_stats_h:
                    s = s.replace('\n','')

                #strip away team data from statbox and remove linebreaks    
                player_stats_a = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[3]/td[1]/descendant::*/text()');
                for s in player_stats_a:
                    s = s.replace('\n','')
                                           

                #strip match stats column
                mstats = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[5]/td/table/tr/td[1]/table/descendant::*/text()')
                for s in mstats:
                    s = s.replace('\n','')
                
                scrapeBasicStats(player_stats_h,str(t),playermatch, "Home")
                scrapeBasicStats(player_stats_a,str(t),playermatch, "Away")
                scrapeQuarters(text_quarters,str(t),quarters)
                scrapeMatchDetails(str(text_details),str(text_result),str(t),mdetails)
                scrapeMatchStats(mstats,str(t),matchstats)
                scrapeVotes(bvotes,str(t),brownlow)
                print("Successfully processed game #" + str(t))
            except:
                print("There was an error with match #" + str(t))
                errorcount += 1 
        else:
            print("Skipping game #" + str(t))
            continue
        
    print("There were " + str(errorcount) + " number of games that failed")    
    return [playermatch,quarters,mdetails,matchstats,brownlow]


def scrapeBasicStats(gameIn,gameID,gameOut, homeAway):
    i = 21
    for x in range(0,22):
        i = i + 30
        hb = int(gameIn[i+4].encode('utf-8'))
        name = str(gameIn[i].encode('utf-8'))[2:-1]
        kicks = int(gameIn[i+2].encode('utf-8'))
        disp = int(gameIn[i+6].encode('utf-8'))
        goals = int(gameIn[i+10].encode('utf-8'))
        behinds = int(gameIn[i+12].encode('utf-8'))
        tackles = int(gameIn[i+14].encode('utf-8'))
        hitouts = int(gameIn[i+16].encode('utf-8'))
        i50s = int(gameIn[i+18].encode('utf-8'))
        freesFor = int(gameIn[i+20].encode('utf-8'))
        freesAgainst = int(gameIn[i+22].encode('utf-8'))
        marks = int(gameIn[i+8].encode('utf-8'))
        AFLfantasy = int(gameIn[i+24].encode('utf-8'))
        Supercoach = int(gameIn[i+26].encode('utf-8'))
        
        gameOut.append({'gameID':gameID, 'homeAway':homeAway, 'name':name, 'kicks':kicks, 
        'handballs':hb, 'disposals':disp,'marks':marks, 
        'goals':goals, 'behinds':behinds, 'tackles':tackles, 
        'hitouts':hitouts, 'i50s':i50s, 'freesFor':freesFor, 
        'freesAgainst':freesAgainst, 'AFLfantasy':AFLfantasy, 'Supercoach':Supercoach})

    
def scrapeQuarters(gameIn,gameID,gameOut):
    i=8
    hq1 = str(gameIn[i+2].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    hq1[1].strip()
    hq1g = int(hq1[0])
    hq1b = int(hq1[1])
    hq1s = (hq1g * 6) + hq1b
    hq2 = str(gameIn[i+3].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    hq2[1].strip()
    hq2g = int(hq2[0])
    hq2b = int(hq2[1])
    hq2s = (hq2g * 6) + hq2b
    hq3 = str(gameIn[i+4].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    hq3[1].strip()
    hq3g = int(hq3[0])
    hq3b = int(hq3[1])
    hq3s = (hq3g * 6) + hq3b
    hq4 = str(gameIn[i+5].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    hq4[1].strip()
    hq4g = int(hq4[0])
    hq4b = int(hq4[1])
    hq4s = (hq4g * 6) + hq4b
    aq1 = str(gameIn[i+10].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    aq1[1].strip()
    aq1g = int(aq1[0])
    aq1b = int(aq1[1])
    aq1s = (aq1g * 6) + aq1b
    aq2 = str(gameIn[i+11].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    aq2[1].strip()
    aq2g = int(aq2[0])
    aq2b = int(aq2[1])
    aq2s = (aq2g * 6) + aq2b
    aq3 = str(gameIn[i+12].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    aq3[1].strip()
    aq3g = int(aq3[0])
    aq3b = int(aq3[1])
    aq3s = (aq3g * 6) + aq3b
    aq4 = str(gameIn[i+13].encode('utf-8'))[2:-1].replace('\\n','').split(".")
    aq4[1].strip()
    aq4g = int(aq4[0])
    aq4b = int(aq4[1])
    aq4s = (aq4g * 6) + aq4b    

    gameOut.append({'gameID':gameID, 
        'homeQ1g':hq1g, 'homeQ1b':hq1b, 'homeQ1s':hq1s,
        'homeQ2g':hq2g, 'homeQ2b':hq2b, 'homeQ2s':hq2s,
        'homeQ3g':hq3g, 'homeQ3b':hq3b, 'homeQ3s':hq3s,
        'homeQ4g':hq4g, 'homeQ4b':hq4b, 'homeQ4s':hq4s,
        'awayQ1g':aq1g, 'awayQ1b':aq1b, 'awayQ1s':aq1s,
        'awayQ2g':aq2g, 'awayQ2b':aq2b, 'awayQ2s':aq2s,
        'awayQ3g':aq3g, 'awayQ3b':aq3b, 'awayQ3s':aq3s,
        'awayQ4g':aq4g, 'awayQ4b':aq4b, 'awayQ4s':aq4s})
        
    
 
def scrapeMatchDetails(gameIn,gameResult,gameID,gameOut):
    gameString = gameIn.replace('\\n','').replace("'",'').split(',')
    mround = gameString[0].split(' ')[1]
    venue = gameString[1]
    crowd = gameString[2].split(' ')[2]
    day = gameString[3]
    #print(gameString)
    date = datetime.strptime(f.changeDate(gameString[4]),'%d %B %Y').date()
    time = str(gameString[5].split(" ")[1] + gameString[5].split(" ")[2] )
    homeodds = gameString[6].split(":")[1].split(" ")[2]
    homeline = gameString[7].split("@")[0].split(" ")[2]
    awayodds = gameString[8].split(":")[1].split(" ")[2]
    awayline = gameString[9].split("@")[0].split(" ")[2]
    
    resultsString = gameResult.replace("'","").replace("defeats","defeated by").replace("defeat ","defeated by").replace("[","").replace("]","").replace("drew with","defeated by")
    results = resultsString.split("defeated by")
    home = results[0]
    away = results[1]
    
    
    
    gameOut.append({'gameID':gameID, 'round':mround.strip(), 'venue':venue.strip(), 'crowd':crowd.strip(),
                    'day':day.strip(), 'date':str(date), 'time':time, 'homeodds':float(homeodds),
                    'homeline':float(homeline), 'awayodds':float(awayodds), 'awayline':float(awayline),
                    'hometeam':home.strip(), 'awayteam':away.strip()})
    
    
def scrapeMatchStats(gameIn,gameID,gameOut):
    home = str(gameIn[3].encode('utf-8'))[2:-1]
    away = str(gameIn[7].encode('utf-8'))[2:-1]
    homekicks = int(gameIn[11].encode('utf-8'))
    awaykicks = int(gameIn[15].encode('utf-8'))
    homehb = int(gameIn[18].encode('utf-8'))
    awayhb = int(gameIn[22].encode('utf-8'))
    homedisp = int(gameIn[25].encode('utf-8'))
    awaydisp = int(gameIn[29].encode('utf-8'))
    homemarks = int(gameIn[39].encode('utf-8'))
    awaymarks = int(gameIn[43].encode('utf-8'))
    hometackles = int(gameIn[46].encode('utf-8'))
    awaytackles = int(gameIn[50].encode('utf-8'))
    homehitout = int(gameIn[53].encode('utf-8'))
    awayhitout = int(gameIn[57].encode('utf-8'))
    homeff = int(gameIn[60].encode('utf-8'))
    awayff = int(gameIn[64].encode('utf-8'))
    homefa = int(gameIn[67].encode('utf-8'))
    awayfa = int(gameIn[71].encode('utf-8'))
    homeg = int(gameIn[74].encode('utf-8'))
    awayg = int(gameIn[78].encode('utf-8'))
    homebk = int(gameIn[81].encode('utf-8'))
    awaybk = int(gameIn[85].encode('utf-8'))
    homerush = int(gameIn[88].encode('utf-8'))
    awayrush = int(gameIn[92].encode('utf-8'))
    homei50 = int(gameIn[123].encode('utf-8'))
    awayi50 = int(gameIn[127].encode('utf-8'))


    gameOut.append({'gameID':gameID, 'hometeam':home.strip(), 'awayteam':away.strip(), 'homekicks':homekicks,
                    'awaykicks':awaykicks, 'homehb':homehb, 'awayhb':awayhb, 'homedisp':homedisp, 'awaydisp':awaydisp,
                    'homemarks':homemarks, 'awaymarks':awaymarks, 'hometackles':hometackles, 'awaytackles':awaytackles,
                    'homehitout':homehitout, 'awayhitout':awayhitout, 'homeff':homeff, 'awayff':awayff,
                    'homefa':homefa, 'awayfa':awayfa, 'homeg':homeg, 'awayg':awayg, 'homebk':homebk, 'awaybk':awaybk,
                    'homerush':homerush, 'awayrush':awayrush, 'homei50':homei50, 'awayi50':awayi50})



def scrapeVotes(gameIn,gameID,gameOut):
    try:
        threevotes = str(gameIn[1].encode('utf-8'))[2:-1]
    except IndexError:
        threevotes = "N/A"
    try:    
        twovotes = str(gameIn[2].encode('utf-8'))[2:-1]
    except IndexError:
        twovotes = "N/A"
    try:
        onevote = str(gameIn[3].encode('utf-8'))[2:-1]
    except IndexError:
        onevote = "N/A"
        
    gameOut.append({'gameID':gameID, 'threevotes':threevotes.strip(), 'twovotes':twovotes.strip(), 'onevote':onevote.strip()})


