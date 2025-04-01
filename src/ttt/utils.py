import typing as ty

import numpy as np


def schedule_from_players(players: ty.List[str]):
    np.random.seed(7)

    matches = []
    for i in range(10):
        # Shuffle players
        np.random.shuffle(players)

        round_x = np.split(np.array(players), 6)

        # Convert back to lists
        round_x = [x.tolist() for x in round_x]
        matches.append(round_x)

    return matches


def standings_from_results(results, players):
    standings = []
    for player in players:
        score = 0
        matches_played = 0
        left_side_instances = [result for result in results if result.player0 == player or result.player1 == player]
        right_side_instances = [result for result in results if result.player2 == player or result.player3 == player]

        # Add scores to each side
        for matches in left_side_instances:
            score += matches.score0
            if matches.score0 != 0 or matches.score1 != 0:
                matches_played += 1

        for matches in right_side_instances:
            score += matches.score1
            if matches.score0 != 0 or matches.score1 != 0:
                matches_played += 1

        standings.append({"name": player, "points": score, "matches_played": matches_played})

    # Sort list by points
    standings.sort(key=lambda x: x["points"], reverse=True)

    # Add rank to dict
    for i, player in enumerate(standings):
        player["rank"] = i + 1

    return standings
