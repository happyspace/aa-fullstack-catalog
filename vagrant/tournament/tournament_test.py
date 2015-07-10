#!/usr/bin/env python
#
# Test cases for tournament.py
from math import log
from math import ceil
import random

from tournament import *


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def test_8_player_no_ties():
    deleteMatches()
    deletePlayers()

    tourney = Tourney.create_tournament("8 player no ties")
    t_id = tourney.id

    registerPlayer("Twilight Sparkle", t_id)
    registerPlayer("Fluttershy", t_id)
    registerPlayer("Applejack", t_id)
    registerPlayer("Pinkie Pie", t_id)
    registerPlayer("Bruno Walton", t_id)
    registerPlayer("Boots O'Neal", t_id)
    registerPlayer("Cathy Burton", t_id)
    registerPlayer("Diane Grant", t_id)

    standings = playerStandings()
    rounds = int(ceil(log(len(standings), 2)))

    for i in xrange(0, rounds):
        pairings = swissPairings(t_id)
        for p in pairings:
            w = random.randint(0, 1)
            w_id = p[w * 2]
            l_id = p[2 - (w * 2)]
            reportMatch(w_id, l_id)

    standings = playerStandings()
    print "Winner: " + str(standings[0][1]) + " with " + str(standings[0][2]) + " wins."
    if standings[0][2] != 3:
        raise ValueError(
            "After three rounds, one player will be the winner with 3 wins.")
        # one player should be the winner
    print "9. Eight player tournament ends with one player as the winner with 3 wins."


def test_7_player_no_ties():
    deleteMatches()
    deletePlayers()

    tourney = Tourney.create_tournament("7 player no ties")
    t_id = tourney.id

    registerPlayer("Twilight Sparkle", t_id)
    registerPlayer("Fluttershy", t_id)
    registerPlayer("Applejack", t_id)
    registerPlayer("Pinkie Pie", t_id)
    registerPlayer("Bruno Walton", t_id)
    registerPlayer("Boots O'Neal", t_id)
    registerPlayer("Cathy Burton", t_id)
    # registerPlayer("Diane Grant", t_id)

    bye_id = Tourney.add_bye_player(t_id)

    standings = playerStandings()

    rounds = int(ceil(log(len(standings), 2)))

    for i in xrange(0, rounds):
        pairings = swissPairings(t_id)
        for p in pairings:
            w = random.randint(0, 1)
            w_id = p[w * 2]
            l_id = p[2 - (w * 2)]
            if w_id != bye_id:
                reportMatch(w_id, l_id)
            else:
                reportMatch(l_id, w_id)

    standings = playerStandings()
    print "Winner: " + str(standings[0][1]) + " with " + str(standings[0][2]) + " wins."
    if standings[0][2] != 3:
        raise ValueError(
            "After three rounds, one player will be the winner with 3 wins.")
        # one player should be the winner
    print "10. Seven player tournament ends with one player as the winner with 3 wins."


def test_8_player_all_ties():
    deleteMatches()
    deletePlayers()

    tourney = Tourney.create_tournament("7 player no ties")
    t_id = tourney.id

    registerPlayer("Twilight Sparkle", t_id)
    registerPlayer("Fluttershy", t_id)
    registerPlayer("Applejack", t_id)
    registerPlayer("Pinkie Pie", t_id)
    registerPlayer("Bruno Walton", t_id)
    registerPlayer("Boots O'Neal", t_id)
    registerPlayer("Cathy Burton", t_id)
    registerPlayer("Diane Grant", t_id)

    standings = playerStandings()

    rounds = int(ceil(log(len(standings), 2)))

    for i in xrange(0, rounds):
        pairings = swissPairings(t_id)
        for p in pairings:
            w = random.randint(0, 1)
            w_id = p[w * 2]
            l_id = p[2 - (w * 2)]

            reportMatch(w_id, l_id, True)

    standings = playerStandings()
    print "Ties: " + str(standings[0][1]) + " with " + str(standings[0][2]) + " wins " + \
          str(standings[0][3]) + " matches."
    if standings[0][2] != 0:
        raise ValueError(
            "After three rounds, no players have a win.")
        # one player should be the winner
    print "11. Eight player tournament ends with all players tied."

def test_7_player_all_ties():
    deleteMatches()
    deletePlayers()

    tourney = Tourney.create_tournament("7 player no ties")
    t_id = tourney.id

    registerPlayer("Twilight Sparkle", t_id)
    registerPlayer("Fluttershy", t_id)
    registerPlayer("Applejack", t_id)
    registerPlayer("Pinkie Pie", t_id)
    registerPlayer("Bruno Walton", t_id)
    registerPlayer("Boots O'Neal", t_id)
    registerPlayer("Cathy Burton", t_id)
    # registerPlayer("Diane Grant", t_id)

    bye_id = Tourney.add_bye_player(t_id)

    standings = playerStandings()

    rounds = int(ceil(log(len(standings), 2)))

    for i in xrange(0, rounds):
        pairings = swissPairings(t_id)
        for p in pairings:
            w = random.randint(0, 1)
            w_id = p[w * 2]
            l_id = p[2 - (w * 2)]
            # byes are counted as a win
            if w_id != bye_id:
                if l_id == bye_id:
                    reportMatch(w_id, l_id, False)
                else:
                    reportMatch(w_id, l_id, True)
            else:
                reportMatch(l_id, w_id, False)

    standings = playerStandings()
    print "Winner: " + str(standings[0][1]) + " with " + str(standings[0][2]) + " wins."
    if standings[0][2] != 1 or standings[1][2] != 1 or standings[2][2] != 1 :
        raise ValueError(
            "After three rounds, there should be three players with one win.")
        # one player should be the winner
    print "12. After three rounds, there should be three players with one win."

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()

    test_8_player_no_ties()
    test_7_player_no_ties()
    test_8_player_all_ties()
    test_7_player_all_ties()


    print "Success!  All tests pass!"


