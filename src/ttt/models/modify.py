from typing import List

from pydantic import UUID4, BaseModel


class TeamScore(BaseModel):
    match_id: UUID4
    team_scores: List[int]
