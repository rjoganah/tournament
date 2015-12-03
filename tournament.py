#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE from players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT count(*) from players")
    count_players = cursor.fetchone()
    DB.close()
    count = int(count_players[0])
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "INSERT INTO players (playerName,wins,matches) VALUES (%s,0,0)",
        (bleach.clean(name),))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT idPlayer,playerName,wins,matches FROM \
        players ORDER BY wins DESC")
    standings = cursor.fetchall()
    DB.commit()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    # We report the match by adding a new match with the winner/loser
    cursor.execute(
        "INSERT INTO matches (winner,loser) VALUES (%s,%s);",
        [winner, loser])
    # We update the wins & matches for the winner
    # We updat the matches for the loser (wins stay the same)
    cursor.execute(
        "UPDATE players SET matches = \
        (select count(*) from matches where winner = %s or loser = %s)\
        , wins = \
        (select count(*) from matches where winner = %s)\
        WHERE idPlayer = %s", [winner, winner, winner, winner])
    cursor.execute(
        "UPDATE players SET matches = \
        (select count(*) from matches where winner = %s or loser = %s)\
        WHERE idPlayer = %s", [loser, loser, loser])
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # get our list of players ordered by wins
    listplayers = playerStandings()
    # new list of paiered players
    swissPairing_players = []
    while(len(listplayers) > 0):
        # Getting the first 2 players on the top of te list
        id1, name1 = listplayers[0][0], listplayers[0][1]
        id2, name2 = listplayers[1][0], listplayers[1][1]
        swissPairing_players.append(
            (
                id1, name1,
                id2, name2
            ))
        # pop the two players already paired
        listplayers.pop(0)
        listplayers.pop(0)
    return swissPairing_players
