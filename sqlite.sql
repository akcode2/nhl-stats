-- This file contains the queries used to construct playoffs.db
-- Schema
Create table for all games
Within the table, have rows for each game
Within each column, have rows for datetime and scoringPlays
Create a new table of scoringPlays
Within scoringPlays have columns for period, periodtime, scoringTeam

CREATE TABLE 

New York Islanders v Carolina Hurricanes
Florida Panthers v Boston Bruins
Minnesota Wild v Dallas Stars
Los Angeles Kings v Edmonton Oilers
New York Rangers v New Jersey Devils
Tampa Bay Lightning v Toronto Maple Leafs
Winnipeg Jets v Vegas Golden Knights
Seattle Kraken v Colorado Avalanche

CREATE TABLE scoring_plays (play_id INTEGER, period INTEGER, period_time TIME, scoring_team TEXT NOT NULL, PRIMARY KEY(id));
CREATE TABLE games (game_id INTEGER, matchup TEXT NOT NULL, game_number INTEGER NOT NULL, datetime DATETIME, scoring_plays INTEGER, FOREIGN KEY (scoring_plays) REFERENCES scoring_plays(id));

CREATE TABLE scoring_plays (
    play_id INTEGER PRIMARY KEY,
    matchup TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    datetime DATETIME, 
    period INTEGER, 
    period_time TIME, 
    scoring_team TEXT NOT NULL
    );