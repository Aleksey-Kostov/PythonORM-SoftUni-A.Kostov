import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Dragon, House, Quest
from django.db import models
from django.db.models import Count, Q


def get_houses(search_string=None):
    if search_string is None or search_string == '':
        return 'No houses match your search.'
    else:
        houses = House.objects.filter(Q(name__istartswith=search_string) | Q(motto__istartswith=search_string))
    if houses:
        houses = houses.order_by('-wins', 'name')
        result = [f"House: {house.name}, wins: {house.wins}, motto: {house.motto or 'N/A'}" for house in houses]
        return '\n'.join(result)
    else:
        return "No houses match your search."


def get_most_dangerous_house():
    try:
        house = House.objects.annotate(num_dragons=Count('house_dragons')).order_by('-num_dragons', 'name').first()
        if house:
            return (f"The most dangerous house is the House of {house.name} with {house.house_dragons.count()} "
                    f"dragons. Currently {'ruling' if house.is_ruling else 'not ruling'} the kingdom.")
        if house is None or house.num_dragons == 0:
            return "No relevant data."
    except AttributeError:
        return "No relevant data."


def get_most_powerful_dragon():
    try:
        dragon = (Dragon.objects.filter(is_healthy=True)
                  .annotate(num_quests=Count('dragons_quest'))
                  .order_by('-power', 'name').first())
        if dragon:
            return (f"The most powerful healthy dragon is {dragon.name} with a power level of {dragon.power:.1f},"
                    f" breath type {dragon.breath}, and {dragon.wins} wins, coming from "
                    f"the house of {dragon.house.name}. "
                    f"Currently participating in {dragon.num_quests} quests.")
        else:
            return "No relevant data."
    except AttributeError:
        return "No relevant data."


def update_dragons_data():
    injured_dragons = Dragon.objects.filter(is_healthy=False)
    for dragon in injured_dragons:
        if dragon.power > 1.0:
            dragon.power = round(max(1.0, dragon.power - 0.1), 1)
            dragon.is_healthy = True
    affected_dragons = Dragon.objects.filter(is_healthy=False, power__gt=1.0)
    min_power = round(affected_dragons.aggregate(min_power=Min('power'))['min_power'], 1)
    if affected_dragons.count() > 0:
        return f"The data for {affected_dragons.count()} dragon/s has been changed. The minimum power level among all dragons is {min_power}"
    else:
        return "No changes in dragons data."


def get_earliest_quest():
    earliest_quest = Quest.objects.order_by('start_time').first()
    if earliest_quest:
        dragons = earliest_quest.dragons.all().order_by('-power', 'name')
        avg_power = round(earliest_quest.dragons.all().aggregate(avg_power=Avg('power'))['avg_power'], 2)
        return f"The earliest quest is: {earliest_quest.name}, code: {earliest_quest.code}, start date: {earliest_quest.start_time.day}.{earliest_quest.start_time.month}.{earliest_quest.start_time.year}, host: {earliest_quest.host.name}. Dragons: {'*'.join([dragon.name for dragon in dragons])}. Average dragons power level: {avg_power}"
    else:
        return "No relevant data."


def announce_quest_winner(quest_code):
    try:
        quest = Quest.objects.get(code=quest_code)
        winning_dragons = quest.dragons.all().order_by('-power', 'name')
        if winning_dragons:
            winning_dragon = winning_dragons[0]
            winning_dragon.wins += 1
            winning_dragon.house.wins += 1
            quest.delete()
            return f"The quest: {quest.name} has been won by dragon {winning_dragon.name} from house {winning_dragon.house.name}. The number of wins has been updated as follows: {winning_dragon.wins} total wins for the dragon and {winning_dragon.house.wins} total wins for the house. The house was awarded with {quest.reward} coins."
        else:
            return "No such quest."
    except Quest.DoesNotExist:
        return "No such quest."
