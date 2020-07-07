#!/usr/bin/env pyton3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:34:20 2020

@author: chris
"""
from resources.team_name_map import team_name_map
import pandas as pd
from os.path import (
    dirname,
    abspath
)
import math

home_dir = dirname(dirname(abspath(__file__)))
matches = pd.read_csv(home_dir + "/bench/matches.csv")

def standardise_teams(fixture: pd.DataFrame):
    """
    Update team names to match those used throughout repo
    """
    for idx,row in fixture.iterrows():
        home = row['hometeam']
        away = row['awayteam']
        if home in team_name_map:
            fixture.at[idx,'hometeam'] = team_name_map[home]
        if away in team_name_map:
            fixture.at[idx,'awayteam'] = team_name_map[away]

    return fixture

def get_winner(homescore,awayscore):
    if homescore > awayscore:
        return 'H'
    elif homescore < awayscore:
        return 'A'
    else:
        return 'D'

def format_fixture(fixture: pd.DataFrame):
    """
    Change the layout of the fixture as it comes in from the web
    """
    fixture.rename(columns={"Round Number": "round", "Date": "date", \
    "Location": "venue", "Home Team": "hometeam", "Away Team": "awayteam"}, \
    inplace = True)
    fixture['homescore'] = None
    fixture['awayscore'] = None
    fixture['winner'] = None
    for idx, row in fixture.iterrows():
        try:
            if math.isnan(row['Result']):
                break
        except TypeError:
            fixture.at[idx,'homescore'] = str(row['Result']).split(' - ')[0]
            fixture.at[idx,'awayscore'] = str(row['Result']).split(' - ')[1]
            fixture.at[idx,'winner'] = get_winner(str(row['Result'].split(' - ')[0]),str(row['Result'].split(' - ')[1]))
    fixture.drop('Result',axis=1,inplace=True)
    return fixture

def fill_fixture_scores(fixture: pd.DataFrame, round_num: int, matches: pd.DataFrame, season: int = 2020):
    """
    Given a round of the season of the fixture, fill out the results of that round
    """
    fixture_round = fixture[fixture['round'] == int(round_num)]

    for idx, row in fixture_round.iterrows():
        match = matches[(matches['hteam'] == row['hometeam']) \
        & (matches['ateam'] == row['awayteam']) \
        & (matches['season'] == season) & (matches['round'] == str(round_num))]
        
        fixture.at[idx,'homescore'] = match['hscore'].iloc[0]
        fixture.at[idx,'awayscore'] = match['ascore'].iloc[0]
        
        if match['hscore'].iloc[0] > match['ascore'].iloc[0]:
            fixture.at[idx,'winner'] = 'H'
        elif match['hscore'].iloc[0] < match['ascore'].iloc[0]:
            fixture.at[idx,'winner'] = 'A'
        else:
            fixture.at[idx,'winner'] = 'D'
            
    return fixture

def get_total_tips(tally: pd.DataFrame):
    """
    Aggregate season tips for each tipster
    """
    tally['total'] = None
    for idx,row in tally.iterrows():
        tally.at[idx,'total'] = row.sum()

    tally.sort_values(by='total', inplace=True, ascending=False)

    return tally

fixture2020 =  pd.read_csv('fixture2020_original.csv')
fixture2020 = format_fixture(fixture2020)
tips2020 =  pd.read_csv('tips2020.csv')
tally2020 =  pd.read_csv('tally2020.csv',index_col='tipper')

rnd = "2"

tippers = tally2020.index.values

fixture2020['key'] = str(fixture2020['round']) + fixture2020['hometeam'] + fixture2020['awayteam']
fixture2020 = standardise_teams(fixture2020)
fixture2020 = fill_fixture_scores(fixture2020, round_num=rnd, matches=matches)
tips2020['key'] = tips2020['round'] + tips2020['hometeam'] + tips2020['awayteam'] 
combined = fixture2020.merge(tips2020,on='key',how='inner')

for tipper in tippers:
    score = 0
    games = combined.loc[combined['round_x'] == rnd]
    for index, row in games.iterrows():
        if(row[tipper] == row['winner']):
           score += 1
    tally2020.at[tipper,"r"+rnd] = score

fixture2020.drop('key',inplace=True,axis=1)
tally2020 = get_total_tips(tally2020)
fixture2020.to_csv('fixture2020.csv')
tally2020.to_csv('tally2020.csv')