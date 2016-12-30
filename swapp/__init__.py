from django.db.backends.signals import connection_created
from django.dispatch import receiver

from swapp.gmaps_api_utils import compute_distance
from items.db_functions import *


@receiver(connection_created)
def extend_db_functions(connection=None, **kwargs):
    connection.connection.create_function("compute_distance", 4, compute_distance)
    connection.connection.create_function("distance_points", 1, distance_points)
