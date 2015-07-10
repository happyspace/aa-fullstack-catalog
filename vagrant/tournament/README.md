## Swiss Style Tournament Project

An implementation of a Swiss Style tournament see [Wikipedia Swiss-system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament). 

`tournament.py` implements each of the API as defined for the project. `tournament.sql` implements a Postgres database
schema see below from a database diagram. 
 
This implementation has the following features. 

1. Support multiple tournaments.
2. Support an odd number of players.
3. Players will not have rematches with a tournament.
4. Draws are possible.
5. Ties are broken according to OMW (Opponent Match Wins). 

### Running the Project

This implementation uses the default API as defined in the project. All additions to the API are implemented as default parameters. 
All original tests run without modification. Additional tests have been added to exercise extra functionality. 

`tournament_test.py` contains the original tests and four new tests.  

These tests are as follows:  

* `test_8_player_no_ties()`  
Run a complete Swiss Style tournament from eight players.  
* `test_7_player_no_ties()`  
Run a complete tournament with an odd number of players. 
* `test_8_player_all_ties()`  
Run a complete tournament with all ties. Players do not have rematches.
* `test_7_player_all_ties()`  
Run a complete tournament with all ties for an odd number of players. Players who receive a bye will end up winning. 

Currently, the API assumes that matches that record a 'bye' are created correctly with the 'bye' player recorded as the loser. 
See source for the tests listed above for examples. 

#### Running the Project

`python tournament_test.py`

### Database Schema

![Database Schema](https://github.com/happyspace/aa-fullstack-nanodegree-vm/blob/master/vagrant/tournament/images/schema.png)
