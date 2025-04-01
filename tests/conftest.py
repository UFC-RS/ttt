import random

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ttt.models as models
import ttt.schemas.orm as orm


@pytest.fixture
def player_names():
    return [
        "Alice",
        "Bob",
        "Charlie",
        "Dana",
        "Eve",
        "Frank",
        "Grace",
        "Hank",
        "Ivy",
        "Jack",
        "Kara",
        "Leo",
        "Mona",
        "Nate",
        "Olivia",
        "Pete",
        "Quinn",
        "Rachel",
        "Steve",
        "Tina",
        "Uma",
        "Victor",
        "Wendy",
        "Xander",
    ]


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:", echo=True)
    # return create_engine("sqlite:///ttt.db")


@pytest.fixture(scope="session")
def tables(engine):
    orm.Base.metadata.create_all(engine)
    # yield
    # orm.Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # transaction = connection.begin()

    # Bind an individual Session to the connection
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    # transaction.rollback()
    # connection.close()


@pytest.fixture
def tournament(db_session, player_names):
    """Create a full tournament with 24 players, following the correct hierarchy."""

    # Step 1: Create the Tournament
    tournament_data = models.create.Tournament(start_date="2025-02-15", rounds_count=10)
    tournament_model = orm.Tournament(**tournament_data.model_dump())

    db_session.add(tournament_model)
    db_session.commit()

    # Shuffle players for random team assignments
    random.shuffle(player_names)

    rounds = []
    matches = []
    teams = []

    player_iter = iter(player_names)  # Iterator to distribute players to teams

    # Step 2: Create Rounds
    for round_number in range(1, tournament_data.rounds_count + 1):
        round_data = models.create.Round(round_number=round_number, tournament_id=tournament_model.id)
        round_model = orm.Round(**round_data.model_dump())

        db_session.add(round_model)
        db_session.commit()
        rounds.append(round_model)

        # Step 3: Create Matches (6 matches per round, 12 teams total)
        round_matches = []
        for match_number in range(6):
            match_data = models.create.Match(round_id=round_model.id)
            match_model = orm.Match(**match_data.model_dump())

            db_session.add(match_model)
            db_session.commit()
            round_matches.append(match_model)

        matches.extend(round_matches)

        # Step 4: Create Teams and assign them to Matches
        round_teams = []
        for match_model in round_matches:
            # Each match gets 2 teams
            team1_data = models.create.Team(round_id=round_model.id, match_id=match_model.id)
            team1_model = orm.Team(**team1_data.model_dump())

            team2_data = models.create.Team(round_id=round_model.id, match_id=match_model.id)
            team2_model = orm.Team(**team2_data.model_dump())

            db_session.add(team1_model)
            db_session.add(team2_model)
            db_session.commit()

            round_teams.append(team1_model)
            round_teams.append(team2_model)

        teams.extend(round_teams)

    # Step 5: Assign Players to Teams (2 players per team, 24 players total)
    for team_model in teams:
        player1_name = next(player_iter, f"Player_{len(teams)}")
        player2_name = next(player_iter, f"Player_{len(teams) + 1}")

        player1_data = models.create.Player(name=player1_name)
        player1_model = orm.Player(**player1_data.model_dump())
        player1_model.teams.append(team_model)

        player2_data = models.create.Player(name=player2_name)
        player2_model = orm.Player(**player2_data.model_dump())
        player2_model.teams.append(team_model)

        db_session.add(player1_model)
        db_session.add(player2_model)

    db_session.commit()

    return tournament_model  # Return the created tournament


@pytest.fixture
def tournament_model(tournament):
    return models.read.Tournament.model_validate(tournament)


@pytest.fixture
def round_model(tournament_model):
    return tournament_model.rounds[0]
