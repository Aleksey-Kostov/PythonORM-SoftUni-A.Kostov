import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
from django.db.models import Count


# Create and run your queries within functions


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""
    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name, country__icontains=search_country)
    elif search_name is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name)
    else:
        players = TennisPlayer.objects.filter(country__icontains=search_country)

    if not players:
        return ""

    players = players.order_by('ranking')
    result = []
    [result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")
     for player in players]
    return '\n'.join(result)


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    if player is None:
        return ''
    return f"Top Tennis Player: {player.full_name} with {player.wins_count} wins."


def get_tennis_player_by_matches_count():
    player_with_most_matches = TennisPlayer.objects \
        .annotate(num_matches=Count('matches')) \
        .order_by('-num_matches', 'ranking') \
        .first()

    if player_with_most_matches is not None and player_with_most_matches.num_matches:
        return f"Tennis Player: {player_with_most_matches.full_name} with " \
               f"{player_with_most_matches.num_matches} matches played."
    return ""


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''
    matching_tournaments = Tournament.objects.prefetch_related('matches') \
        .annotate(num_matches=Count('matches')) \
        .filter(surface_type__icontains=surface) \
        .order_by('-start_date')

    result = []
    [result.append(f"Tournament: {tournament_info.name}, start date: {tournament_info.start_date}, "
                   f"matches: {tournament_info.num_matches}") for tournament_info in matching_tournaments]

    return '\n'.join(result) if result else ''


def get_latest_match_info():
    latest_match = Match.objects \
        .prefetch_related('players') \
        .order_by('-date_played', '-id') \
        .first()

    if latest_match is None:
        return ""

    players = latest_match.players.order_by('full_name')
    player1_full_name = players.first().full_name
    player2_full_name = players.last().full_name
    winner_full_name = "TBA" if latest_match.winner is None else latest_match.winner.full_name

    return f"Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, " \
           f"score: {latest_match.score}, players: {player1_full_name} vs {player2_full_name}, " \
           f"winner: {winner_full_name}, summary: {latest_match.summary}"


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.select_related('tournament', 'winner') \
        .filter(tournament__name__exact=tournament_name) \
        .order_by('-date_played')

    if not matches:
        return "No matches found."

    match_info = []
    [match_info.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {match.winner.full_name if match.winner else 'TBA'}") for match in matches]

    return '\n'.join(match_info)

# print(get_tennis_players(search_name='g', search_country=None))
# print(get_top_tennis_player())
# print(get_tennis_player_by_matches_count())
# print(get_tournaments_by_surface_type('ha'))
# print(get_latest_match_info())
# print(get_matches_by_tournament('French Open 2023'))
# print(get_matches_by_tournament(''))
#
# print(TennisPlayer.objects.get_tennis_players_by_wins_count())
