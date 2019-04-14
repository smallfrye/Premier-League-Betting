#import os

my_os = os.getcwd()
#print(my_os)

import pandas as pd 
import numpy as np 
import math 

# reading the 2018/2019 season data into a dataframe
pl_20182019_data = pd.read_csv('20182019.csv')

# run below to see the first few lines of the dataframe
#print(pl_20152016_data.head())

# dropping unnecessary columns
columns_for_model = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H',\
    'B365D', 'B365A']

# new datframe just with the columns from above
pl_1819_model_data = pl_20182019_data.copy()
pl_1819_model_data = pl_20182019_data.loc[:, columns_for_model]


# The first step is to calculate the average number of goals each team 
# is expected to score in a match.

# To do this each team must be assigned a value for attacking and 
# defensive strength.

# We will use the data from the 2015/2016 season to calculate attack
# and defense strength.

# Iterating over matches to grab some variables re: games played, scoring
total_goals_scored_home = 0
total_goals_scored_away = 0

# count of games played home and away
games_played_home = 0
games_played_away = 0

for match in pl_1819_model_data.itertuples():
    # assign home & away columns to variables
    home_team = match[2]
    away_team = match[3]
    # assign FTHG and FTAG to variables
    home_goals = match[4]
    away_goals = match[5]
    #
    total_goals_scored_home += home_goals
    total_goals_scored_away += away_goals
    # increment games played home & away for each row
    games_played_home += 1
    games_played_away += 1

# Calculating average number of goals scored per game - for both home 
# & away teams for the entire league
avg_goals_scored_home = total_goals_scored_home / games_played_home
avg_goals_scored_away = total_goals_scored_away / games_played_away

print("The average number of goals scored by the home team: %s" % round(avg_goals_scored_home, 3))
print("The average number of goals scored by the away team: %s" % round(avg_goals_scored_away, 3))

# Next we need to determine the average number of goals conceded - for both
# home and away teams for the entire league
# This is easy because it just the opposite of the calculations just made
avg_goals_conced_home = avg_goals_scored_away
avg_goals_conced_away = avg_goals_scored_home

print("The average number of goals conceded by the home team: %s" % round(avg_goals_conced_home, 3))
print("The average number of goals conceded by the away team: %s" % round(avg_goals_conced_away, 3))

# Determine attack and defensive strength for Crystal Palace and Man City
h_team = 'Crystal Palace'
h_team_games_played = 0
h_team_goals_scored = 0

for host in pl_1819_model_data.itertuples():
    if host[2] == h_team:
        h_team_goals_scored += host[4]
        h_team_games_played += 1

h_team_avg_goals_scored = h_team_goals_scored / h_team_games_played
print("Average goals scored at home by %s is: %s" % (h_team, round(h_team_avg_goals_scored, 3)))

# Calculate home team attack strength
h_team_attack_strength = h_team_avg_goals_scored / avg_goals_scored_home
print("%s attack strength is: %s" % (h_team, round(h_team_attack_strength, 3)))

# Calculate away team goals conceded average
a_team = 'Man City'
a_team_games_played = 0
a_team_goals_conced = 0

for visitor in pl_1819_model_data.itertuples():
    if visitor[3] == a_team:
        a_team_goals_conced += visitor[4]
        a_team_games_played += 1

a_team_avg_goals_conced = a_team_goals_conced / a_team_games_played
print("Average goals conceded when away by %s is: %s" % (a_team, round(a_team_avg_goals_conced, 3)))

# Calculate defensive strength of away team
a_team_defense_strength = a_team_avg_goals_conced / avg_goals_conced_away
print("%s defensive strength is: %s" % (a_team, round(a_team_defense_strength, 3)))

# Projecting expected home team goals
exp_home_team_goals = h_team_attack_strength * a_team_defense_strength * avg_goals_scored_home
print("%s expected home team goals: %s" % (h_team, round(exp_home_team_goals, 3)))

# Calculating average goal scoring by away team
a_team_goals_scored = 0 # number of goals scored by away team

for visitor_score in pl_1819_model_data.itertuples():
    if visitor_score[3] == a_team:
        a_team_goals_scored += visitor_score[5]

a_team_avg_goals_scored = a_team_goals_scored / a_team_games_played
print("Average goals scored on the road by %s is %s" % (a_team, round(a_team_avg_goals_scored, 3)))

# Calculate attacking strength of the away team
a_team_attack_strength = a_team_avg_goals_scored / avg_goals_scored_away
print("%s attacking strength when on the road is: %s" % (a_team, round(a_team_attack_strength, 3)))

# Calculating average goal conceded by home team
h_team_goals_conced = 0

for host_conced in pl_1819_model_data.itertuples():
    if host_conced[2] == h_team:
        h_team_goals_conced += host_conced[5]

h_team_avg_goals_conced = h_team_goals_conced / h_team_games_played

print("Average goals conceded at home by %s is %s" % (h_team, round(h_team_avg_goals_conced, 3)))

# Calculate home team defensive strength
h_team_defense_strength = h_team_avg_goals_conced / avg_goals_conced_home
print("%s defensive strength at home is: %s" % (h_team, round(h_team_defense_strength, 3)))

# Projecting expected away team goals
exp_away_team_goals = a_team_attack_strength * h_team_defense_strength * avg_goals_scored_away
print("%s expected away team goals: %s" % (a_team, round(exp_away_team_goals, 3)))

# Use Poisson distribution to predict match outcome
def poisson(actual, mean):
    return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)

max_likelihood = 0

home_win_prob = 0
draw_win_prob = 0
away_win_prob = 0

total_games_simulated = 0
for i in range(10):
    for j in range(10):
        prob = poisson(i, exp_home_team_goals) * poisson(j, exp_away_team_goals)
        
        if prob > max_likelihood:
            max_likelihood = prob
        else:
            pass

        # 
        home_goals_p = i
        away_goals_p = j

        if home_goals_p > away_goals_p:
            home_win_prob += prob
        elif home_goals_p == away_goals_p:
            draw_win_prob += prob
        elif home_goals_p < away_goals_p:
            away_win_prob += prob
        #print("The prob of %s:%s = %s%%" % (i, j, round(prob, 4) * 100))

print("The maximum likelihood is %s%%" % (round(max_likelihood, 4) * 100))
#print("%s wins %s%% of the total games" % (h_team, round(home_team_wins / total_games_simulated, 4) * 100))
#print("%s wins %s%% of the total games" % (a_team, round(away_team_wins / total_games_simulated, 4) * 100))
#print("The teams draw %s%%" % round(draws / total_games_simulated, 4) * 100)
print('%s%% Home Win Prob, %s%% Draw Prob, %s%% Away Win Prob' % \
    (round(home_win_prob, 4) * 100, round(draw_win_prob, 4) * 100, \
        round(away_win_prob, 4) * 100))


