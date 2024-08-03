import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, Sum


def get_astronauts(search_string=None):
    if search_string is None:
        return ''
    if search_string:
        astronauts = Astronaut.objects.filter(Q(name__icontains=search_string) |
                                              Q(phone_number__icontains=search_string)).order_by('name')
    else:
        return ''

    if not astronauts:
        return ''

    result = []

    [result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, "
                   f"status: {'Active' if a.is_active == True else 'Inactive'}") for a in astronauts]

    return '\n'.join(result)


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.num_missions == 0:
        return 'No data.'

    return f"Top Astronaut: {astronaut.name} with {astronaut.num_missions} missions."


def get_top_commander():
    astronaut = (Astronaut.objects.annotate(num_commanded_missions=Count('commander_missions'))
                 .order_by('-num_commanded_missions', 'phone_number').first())

    if not astronaut or astronaut.num_commanded_missions == 0:
        return 'No data.'

    return f"Top Commander: {astronaut.name} with {astronaut.num_commanded_missions} commanded missions."


def get_last_completed_mission():
    last_mission = (Mission.objects.prefetch_related('astronauts')
                    .select_related('spacecraft', 'commander')
                    .filter(status='Completed')
                    .order_by('-launch_date')
                    .first())

    if last_mission is None:
        return 'No data.'

    astronaut_name = ', '.join(a.name for a in last_mission.astronauts.order_by('name'))

    total_spacewalks = last_mission.astronauts.aggregate(total_spacewalks=Sum('spacewalks'))['total_spacewalks']

    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {last_mission.commander.name if last_mission.commander else 'TBA'}. "
            f"Astronauts: {astronaut_name}. "
            f"Spacecraft: {last_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = (Spacecraft.objects.prefetch_related('spacecraft_missions')
                  .annotate(num_missions=Count('spacecraft_missions'),
                            num_astronauts=Count('spacecraft_missions__astronauts'))
                  .order_by('-num_missions', 'name').first())

    if spacecraft is None or spacecraft.num_missions == 0:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.num_missions} missions, "
            f"astronauts on missions: {spacecraft.num_astronauts}.")


def decrease_spacecrafts_weight():
    try:
        spacecrafts = (Spacecraft.objects.prefetch_related('spacecraft_missions')
                       .annotate(num_mission=Count('spacecraft_missions'))
                       .filter(spacecraft_missions__status='Planned', weight__gte=200))

        if not spacecrafts or spacecrafts.num_mission == 0:
            return 'No changes in weight.'

        total_spacecraft = 0
        current_weight = 0
        avg_weight = 0

        for spacecraft in spacecrafts:
            spacecraft.weight -= 200
            spacecraft.save()
            total_spacecraft += 1
            current_weight += spacecraft.weight

        if current_weight != 0 and current_weight > 0:
            avg_weight = current_weight / total_spacecraft

        else:
            avg_weight = 0

        return (f"The weight of {total_spacecraft} "
                f"spacecrafts has been decreased. "
                f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")
    except Spacecraft.DoesNotExist:
        return 'No changes in weight.'
