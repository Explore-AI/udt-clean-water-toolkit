import os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()
# from app.geospatial.data_managers.twgs_data_manager import TWGS_DataManager
from django.contrib.gis.gdal import DataSource
from utilities.models import DMA

def main():
    #from django.contrib.gis.db.models.functions import Distance
    # logger_first = Logger.objects.first()
    # Logger.objects.annotate(distance=Distance("geometry", logger_first.geometry)).filter(distance__lte=10) # gets all loggers within 10 meters of the first logger

    #from django.contrib.gis.measure import D
    #Logger.objects.filter(geometry__dwithin=(first_trunk_main.geometry, D(m=100)))
    pass


if __name__ == "__main__":
    main()
