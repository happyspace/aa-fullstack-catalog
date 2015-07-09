
import random

from tournament import connect
from tournament import reportMatch
from tournament import registerPlayer
from tournament import Tourney
from tournament_test import testDelete


the_players = [
    (1, 'Jeff'),
    (2, 'Adarsh'),
    (3, 'Amanda'),
    (4, 'Eduardo'),
    (5, 'Philip'),
    (6, 'Jee')
]

player_ids = []


def create_random_matches(player_list, tourney, num_matches):
    """
    :param player_list:
    :param tourney:
    :param num_matches:
    :rtype : object
    """
    num_players = len(player_list)
    t_id = tourney.id
    for i in xrange(num_matches):
        print 'match ' + str(i)
        player1_index = random.randint(0, num_players - 1)
        player2_index = random.randint(0, num_players - 1)
        if player2_index == player1_index:
            player2_index = (player1_index + 1) % num_players
        winner_id = player_ids[player1_index]
        winner_name = player_list[player1_index][1]
        loser_id = player_ids[player2_index]
        loser_name = player_list[player2_index][1]
        reportMatch(winner_id, loser_id, t_id)
        print "%s (id=%s) beat %s (id=%s)" % (
            winner_name,
            winner_id,
            loser_name,
            loser_id)


def setup_players_and_matches():
    testDelete()
    # create a tournament
    tourney = Tourney.create_tournament("One Hundred")
    for player in the_players:
        p_id = registerPlayer(player[1], tourney.id)
        player_ids.append(p_id)

    create_random_matches(the_players, tourney, 100)


if __name__ == '__main__':
    setup_players_and_matches()
