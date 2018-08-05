#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:15:51 2018

@author: chrisstrods

This page scrapes additional data from Footywire tables, and creates
the following files:
    odds_data.csv - odds and line data form matches going back to 2010
    fantasy_scores.csv - supercoach and aflfantasy scores for players
    advanced stats - stats which are not recorded on AFLtables
    
"""


import pandas as pd
from lxml import html
from datetime import datetime
import shared_functions as f
import re
from os.path import dirname, abspath
import os



def loadData(gamerange,playermatch,pma,mdetails):
    errorcount = 0
    d = dirname(dirname(abspath(__file__)))


    for t in range(gamerange[0],gamerange[1]+1):
        if(t>9297 or t<6370 and  t!=6079 and t!=6162):
            try:
                print("Processing game #" + str(t))
                #download file from server


                #url ='http://www.footywire.com/afl/footy/ft_match_statistics?mid=' + str(t)
                file = open(d + "/matchfiles/footywire/footywire" + str(t) + ".html")
                afile = open(d + "/matchfiles/footywire_adv/footywire_adv" + str(t) + ".html")
                #tree = etree.parse(response)
                tree = html.fromstring(file.read())
                atree = html.fromstring(afile.read())


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
                    adv_stats_h = atree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[3]/td/table/tr[3]/td/table/tr[1]/td[1]/descendant::*/text()');
                else:
                    player_stats_h = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[1]/td[1]/descendant::*/text()');
                    adv_stats_h = atree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[1]/td[1]/descendant::*/text()');

                #replace newlines with blanks
                for s in player_stats_h:
                    s = s.replace('\n','')

                for s in adv_stats_h:
                    s = s.replace('\n','') 
                    
                



                #strip away team data from statbox and remove linebreaks
                if(year < 2010):
                    player_stats_a = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[3]/td/table/tr[3]/td/table/tr/td/table/tr/td[1]/table/tr[3]/td/table/descendant::*/text()');
                    adv_stats_a = atree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[3]/td/table/tr[3]/td/table/tr/td/table/tr/td[1]/table/tr[3]/td/table/descendant::*/text()');
                else:
                    player_stats_a = tree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[3]/td[1]/descendant::*/text()');
                    adv_stats_a = atree.xpath('//table[@id="frametable2008"]/tr[3]/td[3]/table/tr[4]/td/table/tr[3]/td/table/tr[3]/td[1]/descendant::*/text()');
                for s in player_stats_a:
                    s = s.replace('\n','')
                    
                #replace newlines with blanks
                for s in player_stats_a:
                    s = s.replace('\n','')
                for s in adv_stats_a:
                    s = s.replace('\n','') 



                scrapeBasicStats(player_stats_h,str(t),playermatch, "Home", year)
                scrapeBasicStats(player_stats_a,str(t),playermatch, "Away", year)
                scrapeAdvStats(adv_stats_h,str(t),pma, "Home", year)
                scrapeAdvStats(adv_stats_a,str(t),pma, "Away", year)

                scrapeMatchDetails(str(text_details),str(text_result),str(t),mdetails)
                print("Successfully processed game #" + str(t))
            except IndexError:
                print("There was an index error with match #" + str(t))
                errorcount += 1
        else:
            print("Skipping game #" + str(t))
            continue

    print("There were " + str(errorcount) + " number of games that failed")
    return playermatch,mdetails,pma


def scrapeAdvStats(gameIn,gameID,gameOut, homeAway,year):
    CP,UP,ED,DE,CM,GA,MI5,P1,BO,CCL,SCL,SI,MG,TO,ITC,T5 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    
    i=21
    
    
    for x in range(0,22):
        if(year < 2015):
            i = i + 24
            name = re.sub(r'[^\w\s]','',str(gameIn[i].encode('utf-8'))[2:-1])
            CP = int(gameIn[i+2].encode('utf-8'))
            UP = int(gameIn[i+4].encode('utf-8'))
            ED = int(gameIn[i+6].encode('utf-8'))
            DE = float(gameIn[i+8].encode('utf-8'))
            CM = int(gameIn[i+10].encode('utf-8'))
            GA = int(gameIn[i+12].encode('utf-8'))
            MI5 = int(gameIn[i+14].encode('utf-8'))
            P1 = int(gameIn[i+16].encode('utf-8'))
            BO = int(gameIn[i+18].encode('utf-8'))

        else:
            i = i + 38
            name = re.sub(r'[^\w\s]','',str(gameIn[i].encode('utf-8'))[2:-1])
            CP = int(gameIn[i+2].encode('utf-8'))
            UP = int(gameIn[i+4].encode('utf-8'))
            ED = int(gameIn[i+6].encode('utf-8'))
            DE = float(gameIn[i+8].encode('utf-8'))
            CM = int(gameIn[i+10].encode('utf-8'))
            GA = int(gameIn[i+12].encode('utf-8'))
            MI5 = int(gameIn[i+14].encode('utf-8'))
            P1 = int(gameIn[i+16].encode('utf-8'))
            BO = int(gameIn[i+18].encode('utf-8'))
            CCL = int(gameIn[i+20].encode('utf-8'))  
            SCL = int(gameIn[i+22].encode('utf-8'))  
            SI = int(gameIn[i+24].encode('utf-8'))  
            MG = int(gameIn[i+26].encode('utf-8'))  
            TO = int(gameIn[i+28].encode('utf-8'))  
            ITC = int(gameIn[i+30].encode('utf-8'))  
            T5 = int(gameIn[i+32].encode('utf-8'))  
            
            
        gameOut.append({'gameID':gameID, 'homeAway':homeAway,
            'name':name, 'CP':CP, 'UP':UP,'ED':ED,'DE':DE,'CM':CM,
            'GA':GA,'MI5':MI5,'P1':P1,'BO':BO,'CCL':CCL,'SCL':SCL,
            'SI':SI,'MG':MG,'TO':TO,'ITC':ITC,'T5':T5})
    

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

        kicks = int(gameIn[i+2].encode('utf-8'))

        if(year<2007):
            AFLfantasy = ""
            Supercoach = ""
            continue
        else:
            AFLfantasy = int(gameIn[i+32].encode('utf-8'))
            Supercoach = int(gameIn[i+34].encode('utf-8'))


        gameOut.append({'gameID':gameID, 'homeAway':homeAway,
                        'name':name, 'kicks':kicks, 'AFLfantasy':AFLfantasy,
                        'Supercoach':Supercoach})


def scrapeMatchDetails(gameIn,gameResult,gameID,gameOut):
    gameString = gameIn.replace('\\n','').replace("'",'').split(',')
    
    mround = gameString[0].split(' ')[1]
    if(not(int(gameID) < 1840)):

        date = datetime.strptime(f.changeDate(gameString[4]),'%d %B %Y').date()
        time = str(gameString[5].split(" ")[1] + gameString[5].split(" ")[2] )



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


def main(scode,ecode):
    #used to store the lists
    playermatch = []
    playermatch_adv = []
    mdetails = []
    
    
    d = dirname(dirname(abspath(__file__)))
    daterange = [scode,ecode]

    #4961 - Round one 2010
    #9531 - 2017 GF
    #9567 - End round 6 2018
    #9576 - End round 7 2018


    playermatch,mdetails,playermatch_adv = loadData(daterange,playermatch,playermatch_adv,mdetails)



    if(os.path.isfile(d+"/staging/fantasy_scores.csv")):
        pd.DataFrame.from_dict(playermatch).to_csv(d+"/staging/fantasy_scores.csv", mode="a", index = False, header=False)
    else:
        pd.DataFrame.from_dict(playermatch).to_csv(d+"/staging/fantasy_scores.csv", mode="w", index = False)
    
    if(os.path.isfile(d+"/staging/odds_data.csv")):
        pd.DataFrame.from_dict(mdetails).to_csv(d+"/staging/odds_data.csv", mode="a", index = False, header=False)
    else:
        pd.DataFrame.from_dict(mdetails).to_csv(d+"/staging/odds_data.csv", mode="w", index = False)
    if(os.path.isfile(d+"/staging/adv_stats.csv")):
        pd.DataFrame.from_dict(playermatch_adv).to_csv(d+"/staging/adv_stats.csv", mode="a", index = False, header=False)
    else:
        pd.DataFrame.from_dict(playermatch_adv).to_csv(d+"/staging/adv_stats.csv", mode="w", index = False)


main(9667,9675)


