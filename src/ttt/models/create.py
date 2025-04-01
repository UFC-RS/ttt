from datetime import date

from pydantic import UUID4, BaseModel, field_serializer


class Tournament(BaseModel):
    start_date: date
    status: str = "ongoing"
    rounds_count: int


class Round(BaseModel):
    round_number: int  # Which round (1-10)
    tournament_id: UUID4  # Foreign key

    @field_serializer("tournament_id")
    def serialize_uuid(self, tournament_id):
        return str(tournament_id)


class Match(BaseModel):
    round_id: UUID4  # Foreign key

    @field_serializer("round_id")
    def serialize_uuid(self, round_id):
        return str(round_id)


class Team(BaseModel):
    match_id: UUID4  # Foreign key

    @field_serializer("match_id")
    def serialize_uuid(self, match_id):
        return str(match_id)


class Player(BaseModel):
    name: str
