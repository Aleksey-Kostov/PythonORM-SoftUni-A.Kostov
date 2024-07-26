import os
import django
from django.db.models import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    if search_name is not None and search_country is not None:
        tennis_players = TennisPlayer.objects.filter(full_name__icontains=search_name,
                                                     country__icontains=search_country).order_by('ranking')

    elif search_name is not None and search_country is None:
        tennis_players = TennisPlayer.objects.filter(full_name__icontains=search_name).order_by('ranking')

    else:
        tennis_players = TennisPlayer.objects.filter(country__icontains=search_country).order_by('ranking')

    if not tennis_players:
        return ''

    result = []

    [result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")
     for player in tennis_players]

    return '\n'.join(result)


def get_top_tennis_player():
    top_tennis_players = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not top_tennis_players:
        return ''

    return f"Top Tennis Player: {top_tennis_players.full_name} with {top_tennis_players.wins_count} wins."


def get_tennis_player_by_matches_count():
    tennis_player = (TennisPlayer.objects.annotate(num_matches=Count('matches'))
                     .order_by('-num_matches', 'ranking').first())

    if tennis_player is not None and tennis_player.num_matches:
        return f"Tennis Player: {tennis_player.full_name} with {tennis_player.num_matches} matches played."

    return ''


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments = (Tournament.objects.prefetch_related('matches').annotate(num_matches=Count('matches'))
                   .filter(surface_type__icontains=surface)).order_by('-start_date')

    # print(tournaments)

    if tournaments is None:
        return ''

    result = []

    [result.append(f"Tournament: {t.name}, start date: {t.start_date}, "
                   f"matches: {t.num_matches}") for t in tournaments]

    return '\n'.join(result) if result else ''


def get_latest_match_info():
    latest_match_info = Match.objects.prefetch_related('players').order_by('-date_played', '-id').first()

    # for match in latest_match_info.players.all():
    #     print(match)

    if latest_match_info is None:
        return ''

    players = latest_match_info.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = "TBA" if latest_match_info.winner is None else latest_match_info.winner.full_name

    return (f"Latest match played on: {latest_match_info.date_played}, "
            f"tournament: {latest_match_info.tournament.name}, score: {latest_match_info.score}, players: "
            f"{player1_full_name} vs {player2_full_name}, "
            f"winner: {winner_full_name}, summary: {latest_match_info.summary}")


def get_matches_by_tournament(tournament_name=None):
    match_all = (Match.objects.select_related("tournament", "winner")
                 .filter(tournament__name__exact=tournament_name)
                 .order_by('-date_played'))
    if not match_all:
        return 'No matches found.'

    result = []

    [result.append(f"Match played on: {m.date_played}, score: {m.score}, "
                   f"winner: {'TBA' if not m.winner else m.winner.full_name}") for m in match_all]

    return '\n'.join(result)
