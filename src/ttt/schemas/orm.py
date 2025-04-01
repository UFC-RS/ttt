import uuid

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Function to generate UUIDs
def get_uuid():
    return str(uuid.uuid4())


# Association table for Player-Team many-to-many relationship
player_team_association = Table(
    "player_team",
    Base.metadata,
    Column("player_id", String, ForeignKey("players.id"), primary_key=True),
    Column("team_id", String, ForeignKey("teams.id"), primary_key=True),
)


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(String, primary_key=True, default=get_uuid)
    start_date = Column(Date, nullable=False)
    status = Column(String, default="ongoing")  # ongoing, completed
    rounds_count = Column(Integer, default=10)
    rounds = relationship("Round", back_populates="tournament", cascade="all, delete-orphan")


class Round(Base):
    __tablename__ = "rounds"
    id = Column(String, primary_key=True, default=get_uuid)
    round_number = Column(Integer, nullable=False)
    tournament_id = Column(String, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="rounds")
    matches = relationship("Match", back_populates="round", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"
    id = Column(String, primary_key=True, default=get_uuid)
    round_id = Column(String, ForeignKey("rounds.id"))

    round = relationship("Round", back_populates="matches")
    teams = relationship("Team", back_populates="match", cascade="all, delete-orphan")


class Team(Base):
    __tablename__ = "teams"
    id = Column(String, primary_key=True, default=get_uuid)
    match_id = Column(String, ForeignKey("matches.id"))
    score = Column(Integer, default=0)  # Score stored in the team

    match = relationship("Match", back_populates="teams")
    players = relationship("Player", secondary=player_team_association, back_populates="teams")


class Player(Base):
    __tablename__ = "players"
    id = Column(String, primary_key=True, default=get_uuid)
    name = Column(String, nullable=False)
    cumulative_score = Column(Integer, default=0)

    teams = relationship("Team", secondary=player_team_association, back_populates="players")
