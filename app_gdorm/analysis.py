import setup
from django.contrib.gis.gdal import DataSource

# from geospatial.data_managers.twgs_data_manager import TWGS_DataManager
from utilities.models import DMA

# https://docs.djangoproject.com/en/4.2/ref/contrib/gis/db-api/#spatial-lookups
# https://docs.djangoproject.com/en/4.2/ref/contrib/gis/geoquerysets/#std-fieldlookup-dwithin


def analysis():
    print("success")


analysis()


# gdf = gdm.gdb_zip_to_gdf_layer(zip_file_path, "wLogger")

# print(fiona.listlayers(zip_path))
# ['wFitting', 'wNetworkMeter_Anno', 'wLogger', 'wNetworkOptValve', 'wCOCI_Select', 'wManifold', 'wConnectionMeter', 'wRemovedWaterDevice', 'wPressureContValve_Anno', 'wTrunkMain', 'wDistributionMain', 'wPreTreatmentMeter', 'wCOCI', 'wControlPillar', 'wConnectionMain', 'wVCAPLink', 'wAbandonedWaterDevice', 'wOnSiteProcessMain', 'wAbandonedWaterMain', 'wPressureFitting', 'wDuct', 'wCustomerValve', 'wPressureContValve', 'wVCAP', 'wHydrant_Anno', 'wBoundaryBox', 'wNetworkMeter', 'wNetworkOptValve_Anno', 'wHydrant', 'wMainsJobs', 'CW_Net_Junctions', 'wChamber', 'wOperationalSite', 'wConsumptionMeter', 'wEndItem', 'wRemovedWaterMain', 'wDistributionMain_Anno', 'wOperationalSite_Anno', 'wLINESTOPCLAMP', 'wTrunkMain_Anno', 'N_1_Desc', 'N_1_E0', 'N_1_E1', 'N_1_EDesc', 'N_1_EStatus', 'N_1_ETopo', 'N_1_FloDir', 'N_1_J0', 'N_1_J1', 'N_1_JDesc', 'N_1_JStatus', 'N_1_JTopo', 'N_1_JTopo2', 'N_1_Props']
