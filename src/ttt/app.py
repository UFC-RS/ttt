from pathlib import Path

from litestar import Litestar, Request, get, post
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.di import Provide
from litestar.response import Redirect, Template
from litestar.template.config import TemplateConfig
from sqlalchemy import func
from sqlalchemy.orm import Session

import ttt.models as models
import ttt.schemas.orm as orm
from ttt.db import get_db_session


def get_templates() -> Path:
    """Provide absolute path to `templates` directory."""
    relative_path = Path(__file__).parent / "./templates"
    absolute_path = relative_path.resolve()
    print(absolute_path)
    return absolute_path


@get("/", dependencies={"db": Provide(get_db_session)})
async def tournaments(db: Session) -> Template:
    result = db.query(orm.Tournament).all()
    tournaments = [models.read.Tournament.model_validate(tournament) for tournament in result]
    return Template("tournaments.html", context={"tournaments": tournaments})


@get("/tournament/{tournament_id:str}", dependencies={"db": Provide(get_db_session)})
async def tournament(db: Session, tournament_id: str) -> Template:
    """Fetches a single tournament and renders its details."""
    result = db.query(orm.Tournament).filter(orm.Tournament.id == tournament_id).first()
    tournament = models.read.Tournament.model_validate(result)
    return Template("tournament.html", context={"tournament": tournament})


@get("/leaderboard", dependencies={"db": Provide(get_db_session)})
async def leaderboard(db: Session) -> Template:
    """Fetches all players sorted by highest score first and renders them in a table."""
    # result = db.query(orm.Player).order_by(orm.Player.cumulative_score.desc()).all()
    result = (
        db.query(orm.Player.id, orm.Player.name, func.coalesce(func.sum(orm.Team.score), 0).label("cumulative_score"))
        .join(orm.player_team_association, orm.Player.id == orm.player_team_association.c.player_id)
        .join(orm.Team, orm.player_team_association.c.team_id == orm.Team.id)
        .group_by(orm.Player.id, orm.Player.name)
        .order_by(func.sum(orm.Team.score).desc())
        .all()
    )
    players = [models.read.Player.model_validate(player._asdict()) for player in result]

    return Template("leaderboard.html", context={"players": players})


@post("/score", dependencies={"db": Provide(get_db_session)})
async def update_score(request: Request, db: Session) -> Redirect:
    """Updates team scores for a given match and redirects back to the tournament page."""
    form_data = await request.form()
    match_score = models.read.MatchScore(
        match_id=form_data["match_id"],
        team_ids=[form_data["team1_id"], form_data["team2_id"]],
        team_scores=[form_data["team1_score"], form_data["team2_score"]],
    )

    match = db.query(orm.Match).filter(orm.Match.id == match_score.match_id).first()

    if not match:
        return Redirect("/leaderboard/?error=Match not found")

    # Ensure both team IDs exist in the match
    teams = (
        db.query(orm.Team)
        .filter(orm.Team.id.in_(match_score.team_ids), orm.Team.match_id == match_score.match_id)
        .all()
    )
    if len(teams) != 2:
        return Redirect("/leaderboard/?error=Invalid teams")

    # Update scores
    for team, new_score in zip(teams, match_score.team_scores):
        team.score = new_score  # Overwrite score

    db.commit()  # Save changes
    return Redirect("/leaderboard/?success=Score updated")


app = Litestar(
    route_handlers=[
        tournaments,
        tournament,
        leaderboard,
        update_score,
    ],
    template_config=TemplateConfig(
        directory=get_templates(),
        engine=JinjaTemplateEngine,
    ),
    debug=True,
)
