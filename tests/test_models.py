import ttt.models as models
import ttt.schemas.orm as orm


# Test to create a complete tournament and read back the data
def test_create_and_read_tournament(db_session, tournament):
    # Step 1: Query the database and convert to Pydantic models for reading
    tournament_from_db = db_session.query(orm.Tournament).filter(orm.Tournament.id == tournament.id).first()

    # Convert the ORM model to the corresponding Pydantic read model
    tournament_read_model = models.read.Tournament.model_validate(tournament_from_db)
    print("Tournament from DB:", tournament_read_model)

    # Step 2: Assert the tournament data is correct
    assert str(tournament_read_model.start_date) == "2025-02-15"
    assert tournament_read_model.rounds_count == 10
    assert tournament_read_model.status == "ongoing"


# Test for reading a round, match, and team with players
def test_read_round_and_nested_models(db_session, tournament):
    # Read back the first round
    round_from_db = db_session.query(orm.Round).filter(orm.Round.tournament_id == tournament.id).first()
    round_read_model = models.read.Round.model_validate(round_from_db)
    print("Round from DB:", round_read_model)

    # Read back matches for the round
    for match in round_read_model.matches:
        print(f"Match {match.id} with {len(match.teams)} teams:")
        for team in match.teams:
            players = ", ".join([player.name for player in team.players])
            print(f"  Team {team.id} with score {team.score} and players: {players}")

    # Assert the round has matches and teams
    assert len(round_read_model.matches) > 0  # Should have matches
    assert len(round_read_model.matches[0].teams) == 2  # Should have two teams per match


# Test for creating a match and updating team scores
def test_update_match_score(db_session, tournament):
    # Get the first match from the first round
    first_round = db_session.query(orm.Round).filter(orm.Round.tournament_id == tournament.id).first()
    match = db_session.query(orm.Match).filter(orm.Match.round_id == first_round.id).first()

    # Update the score for the teams in the match
    match_score_data = models.modify.TeamScore(
        match_id=match.id, team_scores=[3, 2]  # Team 1's score is 3, Team 2's score is 2
    )

    # Step 1: Get the teams for the match
    teams = match.teams
    teams[0].score = match_score_data.team_scores[0]
    teams[1].score = match_score_data.team_scores[1]
    db_session.commit()

    # Step 2: Read back the updated match and teams
    updated_match = db_session.query(orm.Match).filter(orm.Match.id == match.id).first()

    assert updated_match.teams[0].score == 3
    assert updated_match.teams[1].score == 2
