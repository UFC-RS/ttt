from datetime import date
from typing import List

from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator


class Tournament(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    start_date: date
    status: str
    rounds_count: int
    rounds: List["Round"] = Field(..., default_factory=list)


class Round(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    round_number: int
    tournament_id: UUID4
    matches: List["Match"] = Field(..., default_factory=list)


class Match(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    round_id: UUID4
    teams: List["Team"] = Field(..., default_factory=list)
    score: int = 0  # Score is derived from teams


class Team(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    match_id: UUID4
    players: List["Player"] = Field(..., default_factory=list)
    score: int


class Player(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str
    cumulative_score: int


class MatchScore(BaseModel):
    match_id: UUID4
    team_ids: List[UUID4]
    team_scores: List[int]

    @field_validator("match_id", mode="after")
    def match_id_to_str(cls, match_id):
        return str(match_id)

    @field_validator("team_ids", mode="after")
    def team_ids_to_str(cls, team_ids):
        return [str(team_id) for team_id in team_ids]
