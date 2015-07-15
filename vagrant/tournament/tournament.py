#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
from random import shuffle
from math import log, ceil

import psycopg2
from psycopg2._psycopg import Error
from psycopg2.extras import DictCursor, DictRow

# params to attach to Postgres from the vagrant host.
params = {
    'database': 'tournament',
    'user': 'vagrant',
    'password': '',
    'host': 'localhost',
    'port': 5432
}


def connect():
    """Connect to the PostgreSQL database.
    Returns:
        a database connection.
    """
    # worked with psycopg2 2.5. '2.4.5' happen
    # return psycopg2.connect(cursor_factory=DictCursor, **params)
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """
    Remove all the match records from the database.
    In addition remove all tournament records from the database.
    """
    conn = connect()
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute("DELETE FROM STANDINGS;")
    c.execute("DELETE FROM opponents;")
    c.execute("DELETE FROM match;")
    c.execute("DELETE FROM tournament;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM STANDINGS;")
    cur.execute("DELETE FROM opponents;")
    cur.execute("DELETE FROM match;")
    cur.execute("DELETE FROM player;")
    conn.commit()
    conn.close()


def countPlayers(tournament_id=0):
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    c.execute("SELECT count(*) AS count FROM player;")
    count = c.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name, tournament_id=0):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      tournament_id: a specific tournament to register the player.

    Return:
        player_id
    """
    values = (name,)  # be sure to make this a tuple
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        query = "INSERT INTO player (name) VALUES (%s) RETURNING id"
        cursor.execute(query, values)
        p_id = cursor.fetchone()[0]
        # create an entry in standings
        if tournament_id == 0:
            tourney = Tourney.get_open_tournament()
            if tourney is None:
                tourney = Tourney.create_tournament()
            tournament_id = tourney.id
        query = "INSERT INTO standings VALUES (%s, %s)"
        cursor.execute(query, (tournament_id, p_id))
    except Error as error:
        print (error)
    finally:
        conn.commit()
        conn.close()
    return p_id


def playerStandings(tournament_id=0):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []
    if tournament_id == 0:
        tourney = Tourney.get_most_recent()
        tournament_id = tourney.id
    values = (tournament_id, )
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        query = "select * from leader_board(%s)"
        cursor.execute(query, values)
        rows = cursor.fetchall()
        for r in rows:
            standings.append(r.values())

    except Error as error:
        print (error)
    finally:
        conn.commit()
        conn.close()
    return standings


def reportMatch(winner, loser, is_tied=False, tournament_id=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost.
    """
    if tournament_id == 0:
        tourney = Tourney.get_most_recent()
        tournament_id = tourney.id
    conn = connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        values = (tournament_id, winner, loser, is_tied)
        query = "select * from record_match(%s, %s, %s, %s)"
        cursor.execute(query, values)
        # score = cursor.fetchone()[0]
        # print score

    except Error as error:
        print (error)
    finally:
        conn.commit()
        conn.close()


def swissPairings(tournament_id=0):
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
    if tournament_id == 0:
        tourney = Tourney.get_most_recent()
        tournament_id = tourney.id

    swiss_pairings = []
    m_count = Tourney.get_match_count(tournament_id)
    p_count = Tourney.get_player_count(tournament_id)
    # odd number of players add in a bye player
    has_bye = False
    bye_id = 0
    if p_count % 2 != 0:
        bye_id = Tourney.add_bye_player(tournament_id)
        has_bye = True
    standings = playerStandings(tournament_id)

    if len(standings) % 2 != 0:
        bye_id = Tourney.get_bye_player(tournament_id)
        has_bye = True

    # if there are no matches recorded then just shuffle. Round 1.
    if m_count == 0:
        standings = playerStandings(tournament_id)
        shuffle(standings)
        pair = []
        paired = set()
        # support bye
        if has_bye:
            pair.append(bye_id)
            pair.append(Tourney.BYE_PLAYER_NAME)
        for s in standings:
            p_id = s[0]
            if p_id not in paired:
                pair.append(s[0])
                pair.append(s[1])
                paired.add(p_id)
            if len(pair) == 4:
                swiss_pairings.append(pair)
                pair = []

    # next rounds. first round may not have been called
    else:
        p_count = Tourney.get_player_count(tournament_id)
        # odd number of players
        if p_count % 2 != 0:
            # raise error
            raise ValueError("After round one, players must be an even number.")
        standings = playerStandings(tournament_id)
        # deal with bye up front
        # fulfill that players may not have a rematch.
        # * find the highest unpaired player in the standings
        # * find the next highest unpaired player in the standings that the player has not played.
        # standing use OMW as a criteria for ordering see documentation for 'leader_board'.
        opponents = Tourney.get_opponents(tournament_id)
        pair = []
        paired = set()
        # deal with the bye first
        if has_bye and bye_id not in paired:
            bye_opps = opponents.get(bye_id)
            pair.append(bye_id)
            pair.append(Tourney.BYE_PLAYER_NAME)
            paired.add(bye_id)
            for i in range(0, len(standings)):
                bye_o = standings[i]
                bye_o_id = bye_o[0]
                if bye_o_id not in bye_opps:
                    paired.add(bye_o_id)
                    pair.append(bye_o[0])
                    pair.append(bye_o[1])
                    swiss_pairings.append(pair)
                    pair = []
                    break
        # pair up everyone else
        for i in range(0, len(standings)):
            s = standings[i]
            p_id = s[0]
            if p_id not in paired:
                pair.append(s[0])
                pair.append(s[1])
                paired.add(p_id)
                # find a pair
                opps = opponents.get(p_id)
                for j in range(i, len(standings)):
                    o = standings[j]
                    o_id = o[0]
                    if o_id != p_id and \
                                    o_id not in opps and \
                                    o_id not in paired:
                        paired.add(o_id)
                        pair.append(o[0])
                        pair.append(o[1])
                        swiss_pairings.append(pair)
                        pair = []
                        break
    return swiss_pairings


class Tourney(object):
    BYE_PLAYER_NAME = "__BYE__"

    @staticmethod
    def get_open_tournament():
        """
        Get latest open tournament.

        An open tournament may accept new players. An open tournament has not had a match recorded.
        Once the first match has been recorded the tournament may not accept new players.
        From open the tournament moves to the 'current' state.

        Returns (Tourney):
            The most recent tournament in the open state
        """
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        tourney = None
        try:
            query = "SELECT * FROM tournament WHERE first_recorded_match_id IS NULL ORDER BY created DESC"
            cursor.execute(query)
            t_row = cursor.fetchone()
            if t_row is not None:
                tourney = Tourney(**t_row.copy())
        except Error as error:
            print (error)
        finally:
            conn.close()
        return tourney

    @staticmethod
    def get_tourney(tournament_id):
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        tourney = None
        try:
            values = (tournament_id,)
            query = "SELECT * FROM tournament where id = %s ORDER BY created DESC"
            cursor.execute(query, values)
            t_row = cursor.fetchone()
            if t_row is not None:
                tourney = Tourney(**t_row.copy())
        except Error as error:
            print (error)
        finally:
            conn.close()
        return tourney

    @staticmethod
    def get_most_recent():
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        tourney = None
        try:
            query = "SELECT * FROM tournament ORDER BY created DESC"
            cursor.execute(query)
            t_row = cursor.fetchone()
            if t_row is not None:
                tourney = Tourney(**t_row.copy())
        except Error as error:
            print (error)
        finally:
            conn.close()
        return tourney

    @staticmethod
    def get_player_count(tournament_id):
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        tourney = None
        try:
            values = (tournament_id,)
            query = "SELECT * FROM player_count(%s)"
            cursor.execute(query, values)
            count = cursor.fetchone()[0]
        except Error as error:
            print (error)
        finally:
            conn.close()
        return count

    @staticmethod
    def get_match_count(tournament_id):
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            values = (tournament_id,)
            query = "SELECT * FROM match_count(%s)"
            cursor.execute(query, values)
            count = cursor.fetchone()[0]
        except Error as error:
            print (error)
        finally:
            conn.close()
        return count

    @staticmethod
    def add_bye_player(tournament_id):
        # check that there is an odd number of players in the tournament.
        n_player = Tourney.get_player_count(tournament_id)
        if n_player % 2 == 0:
            raise ValueError("Tournament has an even number of players. Cannot add bye player.")
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            values = (tournament_id, Tourney.BYE_PLAYER_NAME)
            query = "SELECT * FROM add_bye_player(%s, %s)"
            cursor.execute(query, values)
            player_id = cursor.fetchone()[0]
        except Error as error:
            print (error)
        finally:
            conn.commit()
            conn.close()
        return player_id

    @staticmethod
    def get_bye_player(tournament_id):
        # check that there is an odd number of players in the tournament.
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            values = (tournament_id,)
            query = "SELECT * FROM get_bye_player(%s)"
            cursor.execute(query, values)
            player_id = cursor.fetchone()[0]
        except Error as error:
            print (error)
        finally:
            conn.commit()
            conn.close()
        return player_id

    @staticmethod
    def get_number_of_rounds(tournament_id):

        n_player = Tourney.get_player_count(tournament_id)
        rounds = int(ceil(log(len(n_player), 2)))

        return rounds

    @staticmethod
    def get_number_of_matches(tournament_id):

        n_player = Tourney.get_player_count(tournament_id)
        rounds = int(ceil(n_player / 2.0))

        return rounds

    @staticmethod
    def get_opponents(tournament_id):
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        opponents = {}
        try:
            values = (tournament_id,)
            query = "SELECT * FROM opponents(%s)"
            cursor.execute(query, values)
            opps = cursor.fetchall()
            if opps is not None:
                for o in opps:
                    p_id = o['player_id']
                    if opponents.has_key(p_id):
                        opponents.get(p_id).add(o['opponent_id'])
                    else:
                        opponents[p_id] = set([o['opponent_id']])
        except Error as error:
            print (error)
        finally:
            conn.close()
        return opponents

    @staticmethod
    def create_tournament(name="Tournament"):
        """
        Adds a tournament to the database
        Args:
            name (str):
        Returns:
            Tourney
        """
        values = (name,)
        conn = connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        tourney = None
        try:
            query = "INSERT INTO tournament (name) VALUES (%s) RETURNING id"
            cursor.execute(query, values)
            tournament_id = cursor.fetchone()[0]
            query = "SELECT * FROM tournament WHERE id = %s"
            cursor.execute(query, (tournament_id,))
            t_row = cursor.fetchone()
            t_dict = t_row.copy()
            tourney = Tourney(**t_dict)
        except Error as error:
            print (error)
        finally:
            conn.commit()
            conn.close()
        return tourney

    def __init__(self, **kwargs):
        """

        :rtype : Tourney
        """
        self._id = kwargs['id']
        self._name = kwargs['name']
        self._created = kwargs['created']
        self._first_recorded_match_id = kwargs['first_recorded_match_id']
        self._last_recorded_match_id = kwargs['last_recorded_match_id']

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, value):
        self._created = value

    @property
    def first_recorded_match_id(self):
        return self._first_recorded_match_id

    @first_recorded_match_id.setter
    def first_recorded_match_id(self, value):
        self._first_recorded_match_id = value

    @property
    def last_recorded_match_id(self):
        return self._last_recorded_match_id

    @last_recorded_match_id.setter
    def last_recorded_match_id(self, value):
        self._first_recorded_match_id = value


