-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- CREATE DATABASE tournament;



-- drop everything

DROP SEQUENCE IF EXISTS outcome_id_seq CASCADE;
DROP TABLE IF EXISTS outcome CASCADE;

DROP TABLE IF EXISTS standings CASCADE;
DROP TABLE IF EXISTS opponents CASCADE;

DROP SEQUENCE IF EXISTS match_id_seq CASCADE;
DROP TABLE IF EXISTS match CASCADE;
-- player
DROP SEQUENCE IF EXISTS player_id_seq CASCADE ;
DROP TABLE IF EXISTS player CASCADE;
-- tournament
DROP SEQUENCE IF EXISTS tournament_id_seq CASCADE;
DROP TABLE IF EXISTS tournament CASCADE;

-- create player
CREATE SEQUENCE player_id_seq;
CREATE TABLE player (
  id  BIGINT NOT NULL PRIMARY KEY DEFAULT nextval('player_id_seq'),
  name TEXT NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create sequence
CREATE SEQUENCE match_id_seq;
CREATE TABLE match (
  id  BIGINT NOT NULL PRIMARY KEY DEFAULT nextval('match_id_seq'),
  -- tournament
  tournament_id INT NOT NULL,
  -- record the time the match was reported.
  recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  -- could also make loser/winner a compound primary key
  --CONSTRAINT winner_exists
  --  FOREIGN KEY (winner_id) REFERENCES player
    -- do not delete players
  --  ON DELETE RESTRICT,
  --CONSTRAINT loser_exists
  --  FOREIGN KEY (loser_id) REFERENCES player
    -- do not delete players
  --  ON DELETE RESTRICT
);

-- create tournament
CREATE SEQUENCE tournament_id_seq;
CREATE TABLE tournament (
  id  BIGINT NOT NULL PRIMARY KEY DEFAULT nextval('tournament_id_seq'),
  name TEXT,
  -- cache this first match here, tournament has officially begun.
  -- supports a invariant that no player can be registered after a match starts.
  first_recorded_match_id BIGINT,
  -- the tournament has officially ended.
  -- note this may not be the championship match
  last_recorded_match_id BIGINT,
  -- record the time the tournament was created.
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

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
  tournament_id BIGINT NOT NULL,
  player_id BIGINT NOT NULL,
  is_bye_player BOOLEAN,
  PRIMARY KEY (tournament_id, player_id),

  CONSTRAINT tournament_exists
    FOREIGN KEY (tournament_id) REFERENCES tournament
    -- do not delete players
    ON DELETE RESTRICT,

  CONSTRAINT player_exists
    FOREIGN KEY (player_id) REFERENCES player
    -- do not delete players
    ON DELETE RESTRICT,
  -- only on bye player per tournament
  CONSTRAINT one_bye
    UNIQUE (tournament_id, is_bye_player)
);

-- create outcomes
CREATE SEQUENCE outcome_id_seq;
CREATE TABLE outcome (
  id INT NOT NULL PRIMARY KEY DEFAULT nextval('outcome_id_seq'),
  name TEXT NOT NULL,
  score INT NOT NULL,
  inverse_id INT NOT NULL
);

-- create opponents
CREATE TABLE opponents (
  tournament_id BIGINT NOT NULL,
  player_id BIGINT NOT NULL,
  match_id BIGINT NOT NULL,
  opponent_id BIGINT NOT NULL,
  player_outcome_id INT NOT NULL,

  PRIMARY KEY (tournament_id, player_id, match_id, opponent_id),

  CONSTRAINT tournament_exists
  FOREIGN KEY (tournament_id) REFERENCES tournament
  -- do not delete players
  ON DELETE RESTRICT,

  CONSTRAINT player_exists
  FOREIGN KEY (player_id) REFERENCES player
  -- do not delete players
  ON DELETE RESTRICT,

  CONSTRAINT opponent_exists
  FOREIGN KEY (opponent_id) REFERENCES player
  -- do not delete players
  ON DELETE RESTRICT,

  CONSTRAINT match_exists
  FOREIGN KEY (match_id) REFERENCES match
  -- do not delete matches
  ON DELETE RESTRICT,

  CONSTRAINT outcome_exists
  FOREIGN KEY (player_outcome_id) REFERENCES outcome
  -- do not delete matches
  ON DELETE RESTRICT
);

-- create types data
insert into outcome (name, score, inverse_id) values ('Win', 2, 2);
insert into outcome (name, score, inverse_id) values ('Loss', 0, 1);
insert into outcome (name, score, inverse_id) values ('Tie', 1, 3);

-- add in constraint
ALTER TABLE outcome ADD FOREIGN KEY  (inverse_id) REFERENCES outcome;

-- create a player to represent a bye
insert into player (name) values ('BYE');

drop view if exists view_winners_counts;
create view view_winners_counts as
  select tournament_id, player_id, count(player_id) wins from opponents
  where player_outcome_id = 1
  group by player_id, tournament_id;

drop view if exists view_loser_counts;
create view view_loser_counts as
  select tournament_id, player_id, count(player_id) losses from opponents
  where player_outcome_id = 2
  group by player_id, tournament_id;

drop view if exists view_tie_counts;
create view view_tie_counts as
  select tournament_id, player_id, count(player_id) tie from opponents
  where player_outcome_id = 3
  group by player_id, tournament_id;

drop view if exists view_opp_winners_counts;
create view view_opp_winners_counts as
  select tournament_id, player_id, count(player_id) opp_score from opponents
  where player_outcome_id = 2
  group by player_id, tournament_id;


create or replace function match_count(tournament_id bigint)
  RETURNS INT AS
  $func$
  DECLARE
      t_id ALIAS FOR $1;
      m_count INT := 0;
  BEGIN
    SELECT INTO m_count count(id) from match m
    WHERE m.tournament_id = t_id;

    RETURN m_count;
  END;
  $func$
LANGUAGE plpgsql;

create or replace function player_count(tournament_id bigint )
    RETURNS INT AS
  $func$
  DECLARE
      t_id ALIAS FOR $1;
      p_count INT := 0;
  BEGIN
    SELECT INTO p_count count(player_id) from standings s
    WHERE s.tournament_id = t_id;

    RETURN p_count;
  END;
  $func$
LANGUAGE plpgsql;

create or replace function get_bye_player(tournament_id bigint)
    RETURNS INT AS
  $func$
  DECLARE
      t_id ALIAS FOR $1;
      p_id INT := 0;
  BEGIN
    SELECT INTO p_id player_id from standings s
    WHERE s.tournament_id = t_id and s.is_bye_player is TRUE;

    RETURN p_id;
  END;
  $func$
LANGUAGE plpgsql;

create or replace function add_bye_player(tournament_id bigint, bye_player_name TEXT)
    RETURNS INT AS
  $func$
  DECLARE
      t_id ALIAS FOR $1;
      p_name ALIAS FOR $2;
      p_id INT := 0;
  BEGIN
    INSERT INTO player (name) values (p_name) returning id into p_id;
    INSERT INTO standings (tournament_id, player_id, is_bye_player) values (t_id, p_id, TRUE);

    RETURN p_id;
  END;
  $func$
LANGUAGE plpgsql;

create or replace function opponents(tournament_id bigint)
  RETURNS TABLE (player_id bigint, opponent_id bigint) AS
  $func$
  DECLARE
      t_id ALIAS FOR $1;
  BEGIN
    return query SELECT o.player_id, o.opponent_id from OPPONENTS o
    WHERE o.tournament_id = t_id
    ORDER BY player_id;
  END;
  $func$
LANGUAGE plpgsql;

-- function that creates match records in a consistent way.
create or replace function record_match(tournament_id bigint,
  winner_id bigint, loser_id bigint, is_tied boolean)

  RETURNS INT AS
  $func$
  DECLARE
    t_id ALIAS FOR $1;
    w_id ALIAS FOR $2;
    l_id ALIAS FOR $3;
    is_tied ALIAS FOR $4;
    -- declare a variable to hold inverse outcome id
    inv_id INT;
    score INT;
    o_id INT := 1;
    m_id INT := 0;
  BEGIN
    IF is_tied = TRUE THEN
      o_id := 3;
    END IF;

    INSERT INTO match (tournament_id) VALUES (t_id) returning id into m_id;

    SELECT INTO inv_id inverse_id FROM outcome
    WHERE id = o_id;
    SELECT INTO score outcome.score FROM outcome
    WHERE id = o_id;
    -- store 'winner'/'loser' record.
    INSERT INTO opponents (tournament_id, match_id,  player_id,
                          opponent_id, player_outcome_id)
    VALUES (t_id, m_id, w_id, l_id, o_id);
    -- store the inverse.
    INSERT INTO opponents (tournament_id, match_id,  player_id,
                          opponent_id, player_outcome_id)
    VALUES (t_id, m_id, l_id, w_id , inv_id);

    RETURN score;
  END;
  $func$
LANGUAGE plpgsql;


create or replace function extended_leader_board(tournament_id bigint)
  RETURNS TABLE (id bigint, name text, wins bigint, matches bigint) AS
  $func$
  DECLARE
    t_id ALIAS FOR $1;
    w_score INT;
    t_score INT;
  BEGIN
    SELECT INTO w_score o.score FROM outcome o
      WHERE o.id = 1;
    SELECT INTO t_score o.score FROM outcome o
      WHERE o.id = 3;

    return query select player_id, player_name, player_wins, player_matches
    from (
         select s.tournament_id, s.player_id, p.name as player_name,
           COALESCE(vwc.wins,0) as player_wins, COALESCE(vlc.losses,0) as losses,
           COALESCE(vtc.tie,0) as tie,
           (COALESCE(vwc.wins,0) * w_score) +  (COALESCE(vtc.tie,0) * t_score)  as score,
           COALESCE(vwc.wins,0) + COALESCE(vlc.losses,0) + COALESCE(vtc.tie,0) as player_matches,
           (COALESCE(vowc.opp_score,0) * w_score) +  (COALESCE(vtc.tie,0) * t_score) as opp_score
         from standings s
           left outer join view_winners_counts vwc on (s.player_id = vwc.player_id) and (s.tournament_id = vwc.tournament_id)
           left outer join view_loser_counts vlc on (s.player_id = vlc.player_id) and (s.tournament_id = vlc.tournament_id)
           left outer join view_tie_counts vtc on (s.player_id = vtc.player_id) and (s.tournament_id = vtc.tournament_id)
           left outer join view_opp_winners_counts vowc on (s.player_id = vowc.player_id) and (s.tournament_id = vowc.tournament_id)
           join player p on (s.player_id = p.id)
         WHERE s.tournament_id = t_id and s.is_bye_player is not TRUE
         order by vwc.tournament_id, score DESC, opp_score DESC) as extended_leader_board;
  END;
  $func$
LANGUAGE plpgsql;


create or replace function leader_board(tournament_id bigint)
  RETURNS TABLE (player_id bigint, player_name text, player_wins bigint, player_matches bigint) AS
  $func$
  DECLARE
    t_id ALIAS FOR $1;
  BEGIN
    return query select id, name, wins, matches
    from (
      select * from extended_leader_board(t_id)
    ) as leader_board;

  END;
  $func$
LANGUAGE plpgsql;









