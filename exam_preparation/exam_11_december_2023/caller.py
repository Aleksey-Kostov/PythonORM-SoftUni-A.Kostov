import os
import django
from django.db.models import Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer


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

