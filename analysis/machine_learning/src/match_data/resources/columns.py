match_columns = [
    'matchid',
    'venue',
    'date',
    'day',
    'time',
    'crowd',
    'umpire1',
    'umpire2',
    'umpire3',
    'umpire1games',
    'umpire2games',
    'umpire3games',
    'hteam',
    'ateam',
    'hscore',
    'ascore'
]

home_team_columns = [
    'hteam',
    'hscore',
    'hteam_q1_goals',
    'hteam_q1_behinds',
    'hteam_q1_score',
    'hteam_q2_goals',
    'hteam_q2_behinds',
    'hteam_q2_score',
    'hteam_q3_goals',
    'hteam_q3_behinds',
    'hteam_q3_score',
    'hteam_q4_goals',
    'hteam_q4_behinds',
    'hteam_q4_score',
    'hteam_et',
    'homeodds',
    'homeline'
]

away_team_columns = [
    'ateam',
    'ascore',
    'ateam_q1_goals',
    'ateam_q1_behinds',
    'ateam_q1_score',
    'ateam_q2_goals',
    'ateam_q2_behinds',
    'ateam_q2_score',
    'ateam_q3_goals',
    'ateam_q3_behinds',
    'ateam_q3_score',
    'ateam_q4_goals',
    'ateam_q4_behinds',
    'ateam_q4_score',
    'ateam_et',
    'awayodds',
    'awayline'
]

generic_team_columns = [
    'team',
    'score',
    'q1_goals',
    'q1_behinds',
    'q1_score',
    'q2_goals',
    'q2_behinds',
    'q2_score',
    'q3_goals',
    'q3_behinds',
    'q3_score',
    'q4_goals',
    'q4_behinds',
    'q4_score',
    'et',
    'odds',
    'line'
]

home_cols_mapped = dict(zip(home_team_columns,generic_team_columns))
away_cols_mapped = dict(zip(away_team_columns,generic_team_columns))