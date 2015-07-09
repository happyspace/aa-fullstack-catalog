from tournament import *

def testCreateTournament():
    deleteMatches()
    tourny = Tourney.create_tournament("My First Tournament")
    if tourny is not None:
        print "1. Created tournament. " + str(tourny)


if __name__ == '__main__':
    testCreateTournament()

    print "Success!  All tests pass!"
