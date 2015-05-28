-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- CREATE DATABASE tournament;

-- drop everything
-- player
DROP SEQUENCE IF EXISTS player_id_seq CASCADE ;
DROP TABLE IF EXISTS player CASCADE;
-- tournament
DROP SEQUENCE IF EXISTS tournament_id_seq CASCADE;
DROP TABLE IF EXISTS tournament CASCADE;

DROP TABLE IF EXISTS standings CASCADE;

DROP SEQUENCE IF EXISTS match_id_seq CASCADE;
DROP TABLE IF EXISTS match CASCADE;

-- create player
CREATE SEQUENCE player_id_seq;
CREATE TABLE player (
  id  INT NOT NULL PRIMARY KEY DEFAULT nextval('player_id_seq'),
  name TEXT NOT NULL

);

-- create sequence
CREATE SEQUENCE match_id_seq;
CREATE TABLE match (
  id  INT NOT NULL PRIMARY KEY DEFAULT nextval('match_id_seq'),
  -- tournament
  tournament_id INT NOT NULL,
  -- allow for byes for odd numbers of players
  loser_id INT,
  winner_id INT NOT NULL,
  tie BOOLEAN NOT NULL DEFAULT FALSE,
  -- record the time the match was reported.
  recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- could also make loser/winner a compound primary key
  -- players may not play themselves
  unique (loser_id, winner_id),
  CONSTRAINT winner_exists
    FOREIGN KEY (winner_id) REFERENCES player
    -- do not delete players
    ON DELETE RESTRICT,
  CONSTRAINT loser_exists
    FOREIGN KEY (loser_id) REFERENCES player
    -- do not delete players
    ON DELETE RESTRICT
);

-- create tournament
CREATE SEQUENCE tournament_id_seq;
CREATE TABLE tournament (
  id  INT NOT NULL PRIMARY KEY DEFAULT nextval('tournament_id_seq'),
  name TEXT,
  -- cache this first match here, tournament has officially begun.
  -- supports a invariant that no player can be registered after a match starts.
  first_recorded_match_id INT,
  -- the tournament has officially ended.
  -- note this may not be the championship match
  last_recorded_match_id INT,

  CONSTRAINT first_recorded_match
    FOREIGN KEY (first_recorded_match_id ) REFERENCES match
    -- do not delete players
    ON DELETE RESTRICT,
  CONSTRAINT last_recorded_match
    FOREIGN KEY (last_recorded_match_id ) REFERENCES match
    -- do not delete players
    ON DELETE RESTRICT
);

-- add constraint
ALTER TABLE match ADD FOREIGN KEY  (tournament_id) REFERENCES tournament
    -- do not delete tournaments
    ON DELETE RESTRICT;

-- create standings
CREATE TABLE standings (
  tournament_id INT NOT NULL,
  player_id INT NOT NULL,
  score INT NOT NULL DEFAULT 0,
  PRIMARY KEY (tournament_id, player_id),

  CONSTRAINT tournament_exists
    FOREIGN KEY (tournament_id) REFERENCES tournament
    -- do not delete players
    ON DELETE RESTRICT,

  CONSTRAINT player_exists
    FOREIGN KEY (player_id) REFERENCES player
    -- do not delete players
    ON DELETE RESTRICT
);

drop view if exists view_winners_counts;
create view view_winners_counts as
  select tournament_id, winner_id, count(winner_id) wins from match
  where tie != TRUE
  group by winner_id, tournament_id;

drop view if exists standings_view_winners;
create view standings_view_winners as
  select player.id, player.name, wins
  from player left outer join view_winners_counts vwc on (player.id = vwc.winner_id)










