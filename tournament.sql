-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
    idPlayer SERIAL PRIMARY KEY,
    wins INTEGER,
    matches INTEGER,
    playerName varchar(50)

 );

create table matches (
    idMatch SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES player(idPlayer),
    loser INTEGER REFERENCES player(idPlayer),

);