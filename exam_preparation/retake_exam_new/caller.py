import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Count


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    if search_name is not None and search_country is not None:
        tennis_player = (
            TennisPlayer.objects.filter(country__icontains=search_country, full_name__icontains=search_name)
            .order_by('ranking'))

    elif search_name is not None:
        tennis_player = TennisPlayer.objects.filter(full_name__icontains=search_name).order_by('ranking')

    else:
        tennis_player = TennisPlayer.objects.filter(country__icontains=search_country).order_by('ranking')

    if not tennis_player:
        return ''

    result = []

    [result.append(f"Tennis Player: {tp.full_name}, country: {tp.country}, "
                   f"ranking: {tp.ranking}") for tp in tennis_player]

    return '\n'.join(result)


def get_top_tennis_player():
    tennis_player = (TennisPlayer.objects.annotate(num_wins=Count('winner'))
                     .order_by('-num_wins', 'full_name')
                     .first())

    if not tennis_player:
        return ''

    return f'Top Tennis Player: {tennis_player.full_name} with {tennis_player.num_wins} wins.'


def get_tennis_player_by_matches_count():
    tennis_player = (TennisPlayer.objects.annotate(matches_count=Count('players_matches'))
                     .order_by('-matches_count', 'ranking')
                     .first())

    if not tennis_player or tennis_player.matches_count == 0:
        return ''

    return f"Tennis Player: {tennis_player.full_name} with {tennis_player.matches_count} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''
    tournaments = (Tournament.objects.prefetch_related('tournament_matches')
                   .annotate(num_matches=Count('tournament_matches'))
                   .filter(surface_type__icontains=surface).order_by('-start_date'))

    if not tournaments:
        return ''

    result = []
    [result.append(f"Tournament: {t.name}, start date: {t.start_date}, "
                   f"matches: {t.num_matches}") for t in tournaments]

    return "\n".join(result)


def get_latest_match_info():
    latest_match = (Match.objects.select_related('tournament').prefetch_related('players')
                    .order_by('-date_played', '-id').first())

    if not latest_match:
        return ''

    players = latest_match.players.order_by('full_name')
    player_1 = players.first().full_name
    player_2 = players.last().full_name
    players_full_name = f"{player_1} vs {player_2}"

    return (f"Latest match played on: {latest_match.date_played}, "
            f"tournament: {latest_match.tournament.name}, "
            f"score: {latest_match.score}, players: {players_full_name}, "
            f"winner: {'TBA' if latest_match.winner is None else latest_match.winner.full_name}, "
            f"summary: {latest_match.summary}")


def get_matches_by_tournament(tournament_name=None):

    if tournament_name is None:
        return 'No matches found.'

    matches = (Match.objects.select_related('tournament', 'winner')
               .filter(tournament__name__exact=tournament_name)
               .order_by('-date_played'))

    if not matches:
        return 'No matches found.'

    result = []

    [result.append(f"Match played on: {m.date_played}, score: {m.score}, "
                   f"winner: {'TBA' if not m.winner else m.winner.full_name}") for m in matches]

    return '\n'.join(result)

# print(get_matches_by_tournament('kiro'))