import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()
# from app.geospatial.data_managers.twgs_data_manager import TWGS_DataManager
from django.contrib.gis.gdal import DataSource
from utilities.models import DMA
from assets.models import distribution_main, hydrant, logger, network_meter, trunk_main

# Logger: GISID, DMACODE1, SHAPEX, SHAPEY, geometry


def main():
    pass


if __name__ == "__main__":
    main()
