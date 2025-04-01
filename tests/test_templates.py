import uuid

import pytest
from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.testing import TestClient


@pytest.fixture
def litestar_app(tournament_model):
    """Creates a Litestar app locally within the test"""

    @get("/tournaments")
    async def tournaments_list() -> Template:
        return Template("tournaments.html", context={"tournaments": [tournament_model, tournament_model]})

    @get("/tournament/{tournament_id:str}")
    async def tournament_detail(tournament_id: uuid.UUID) -> Template:
        """Fetches a single tournament and renders its details."""
        return Template("tournament.html", context={"tournament": tournament_model})

    @get("/round/{round_id:str}")
    async def round_detail(round_id: uuid.UUID) -> Template:
        """Fetches a single round and renders its details."""
        return Template("round.html", context={"round": tournament_model.rounds[0]})

    @get("/match/{match_id:str}")
    async def match_detail(match_id: uuid.UUID) -> Template:
        """Fetches a single match and renders its details."""
        return Template("match.html", context={"match": tournament_model.rounds[0].matches[0]})

    # Define the Litestar app
    app = Litestar(
        route_handlers=[
            tournaments_list,
            tournament_detail,
            round_detail,
            match_detail,
        ],
        template_config=TemplateConfig(
            directory="../templates",
            engine=JinjaTemplateEngine,
        ),
    )

    return app


def test_template_tournaments(litestar_app):
    """Runs a local Litestar app and tests template rendering"""

    with TestClient(litestar_app) as client:
        response = client.get("/tournaments")

    assert response.status_code == 200
    assert response.text


def test_template_tournament(litestar_app, tournament_model):
    """Runs a local Litestar app and tests rendering of a single tournament."""

    with TestClient(litestar_app) as client:
        response = client.get(f"/tournament/{tournament_model.id}")

    assert response.status_code == 200
    assert response.text


def test_template_round(litestar_app, round_model):
    """Runs a local Litestar app and tests rendering of a single round."""

    with TestClient(litestar_app) as client:
        response = client.get(f"/round/{round_model.id}")

    assert response.status_code == 200
    assert response.text


def test_template_match(litestar_app, round_model):
    """Runs a local Litestar app and tests rendering of a single round."""

    with TestClient(litestar_app) as client:
        response = client.get(f"/match/{round_model.matches[0].id}")

    assert response.status_code == 200
    assert response.text
