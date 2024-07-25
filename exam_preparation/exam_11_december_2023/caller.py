import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    if search_name is not None and search_country is not None:
        tennis_players = TennisPlayer.objects.filter(full_name__icontains=search_name,
                                                     country__icontains=search_country).ordrer_by('ranking')

    elif search_name is not None and search_country is None:
        tennis_players = TennisPlayer.objects.filter(full_name__icontains=search_name).ordrer_by('ranking')

    else:
        tennis_players = TennisPlayer.objects.filter(country__icontains=search_country).ordrer_by('ranking')

    if not tennis_players:
        return ''

    result = []

    [result.append(f"Tennis Player: {player.full_name}, country: "
                   f"{player.country}, ranking: {player.ranking}") for player in tennis_players]

    return '\n'.join(result)
