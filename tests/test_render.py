from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("../templates"))


def test_render_tournaments(tournament_model):
    """Tests Jinja rendering for a tournaments page."""
    template = env.get_template("tournaments.html")

    rendered_html = template.render(tournaments=[tournament_model, tournament_model])
    assert rendered_html


def test_render_tournament(tournament_model):
    """Tests Jinja rendering for a single tournament page."""
    template = env.get_template("tournament.html")

    rendered_html = template.render(tournament=tournament_model)
    assert rendered_html


def test_render_round(round_model):
    """Tests Jinja rendering for a single round page."""
    template = env.get_template("round.html")

    rendered_html = template.render(round=round_model)
    assert rendered_html


def test_render_match(round_model):
    """Tests Jinja rendering for a single match page."""
    template = env.get_template("match.html")

    rendered_html = template.render(match=round_model.matches[0])
    assert rendered_html
