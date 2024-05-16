import time
from os import makedirs
from os.path import exists, join
from requests import get, exceptions
from utils.utils import GeoServerConfig, DBConnection
from sys import argv


class Downloader:
    def __init__(self):
        self.geoserver_config = GeoServerConfig()
        self.geoserver_auth = self.geoserver_config.geoserver_auth
        self.url_set = set()

    # Function to download and save images from WMS endpoints
    def generate_output(self, url, file_path):
        """"
        Helper function to save the output to a file
        """
        auth = self.geoserver_auth.auth

        if url in self.url_set:  # Check if the URL already exists
            print("Image already downloaded, skipping:", url)
        else:
            try:
                response = get(url, auth=auth)
                response.raise_for_status()
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                file.close()
                self.url_set.add(url)  # Add the URL to the set
            except exceptions.RequestException as e:
                print("Error downloading image:", e)

    # Function to retrieve wms images from published GeoServer layers
    def get_layer_snapshot(self, geoserver_site_url, workspace_name):
        """
        Download the snapshot of the layer based on the Get-map bbox
        Args:
            geoserver_site_url:
            workspace_name:

        Returns:

        """
        auth = self.geoserver_auth.auth
        db_conn = DBConnection()
        pg_tables = db_conn.pg_extent_details()

        if pg_tables:
            for table_name, bbox in pg_tables:
                # Check if the store already exists
                rest_url = '%s/rest/workspaces/%s/datastores/%s.json' % (
                    geoserver_site_url, workspace_name, workspace_name)
                response = get(rest_url, auth=auth)
                response.raise_for_status()
                if response.status_code == 200:
                    layer_url = "%s/rest/workspaces/%s/datastores/%s/featuretypes/%s.json" % (
                        geoserver_site_url, self.geoserver_config.default['GEO_WORKSPACE'],
                        self.geoserver_config.default['GEO_WORKSPACE'], table_name)
                    layer_response = get(layer_url, auth=auth)
                    layer_response.raise_for_status()
                    if layer_response.status_code == 200:
                        get_map_url = '%s/%s/wms?service=WMS&version=1.1.0&request=GetMap&layers=%s:%s&bbox=%s,%s,%s,%s&width=%s&height=%s&srs=EPSG:%s&styles=&format=%s' % (
                            geoserver_site_url, workspace_name, workspace_name, table_name, bbox[0], bbox[1],
                            bbox[2],
                            bbox[3],
                            self.geoserver_config.default['HEIGHT'], self.geoserver_config.default['WIDTH'],
                            bbox[4],
                            self.geoserver_config.default['FORMAT'])
                        image_extension = self.geoserver_config.default['FORMAT'].split('/')[-1]
                        base_path = join("/geoserver_scripts", "output")
                        if not exists(base_path):
                            makedirs(base_path)
                        time_stamp = time.strftime("%Y%m%d-%H%M%S")
                        report_image = f"{table_name}_{time_stamp}.{image_extension}"
                        file_path = join(base_path, report_image)
                        # Download and save the image
                        self.generate_output(get_map_url, file_path)

    def get_layer_snapshot_per_dma(self, geoserver_site_url, workspace_name, codes):
        """
        Download the snapshot of the layer based on the Get-map bbox of a DMA
        Args:
            geoserver_site_url:
            workspace_name:


        Returns:

        """
        auth = self.geoserver_auth.auth
        db_conn = DBConnection()
        spatial_tables = db_conn.pg_spatial_tables()

        if spatial_tables:
            for table_name, geom_type in spatial_tables:

                # Check if the store already exists
                rest_url = '%s/rest/workspaces/%s/datastores/%s.json' % (
                    geoserver_site_url, workspace_name, workspace_name)
                response = get(rest_url, auth=auth)
                response.raise_for_status()
                if response.status_code == 200:
                    layer_url = "%s/rest/workspaces/%s/datastores/%s/featuretypes/%s.json" % (
                        geoserver_site_url, self.geoserver_config.default['GEO_WORKSPACE'],
                        self.geoserver_config.default['GEO_WORKSPACE'], table_name)
                    layer_response = get(layer_url, auth=auth)
                    layer_response.raise_for_status()
                    if layer_response.status_code == 200:
                        dma_codes_list = db_conn.pg_dma_extent_details(codes)
                        for code, coordinates in dma_codes_list:
                            min_x, min_y, max_x, max_y, srid = coordinates
                            # TODO fix bbox assignment
                            get_map_url = '%s/%s/wms?service=WMS&version=1.1.0&request=GetMap&layers=%s:%s&bbox=%s,%s,%s,%s&width=%s&height=%s&srs=EPSG:%s&styles=&format=%s' % (
                                geoserver_site_url, workspace_name, workspace_name, table_name, min_x, min_y,
                                max_x,
                                max_y,
                                self.geoserver_config.default['HEIGHT'], self.geoserver_config.default['WIDTH'],
                                srid,
                                self.geoserver_config.default['FORMAT'])

                            image_ext = self.geoserver_config.default['FORMAT'].split('/')[-1]
                            base_path = join("/geoserver_scripts", "output")
                            if not exists(base_path):
                                makedirs(base_path)
                            time_stamp = time.strftime("%Y%m%d-%H%M%S")
                            report_image = f"{table_name}_{code}_{time_stamp}.{image_ext}"
                            file_path = join(base_path, report_image)
                            # Download and save the image
                            self.generate_output(get_map_url, file_path)

    def geoserver_get_map(self):

        """
        Prints maps in various formats based on get-map requests to the GeoServer service
        Returns:

        """
        self.get_layer_snapshot(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                                self.geoserver_config.default['GEO_WORKSPACE'])

    def dma_get_map(self):

        """
        Prints maps in various formats based on get-map requests to the GeoServer service
        Returns:

        """
        self.get_layer_snapshot_per_dma(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                                        self.geoserver_config.default['GEO_WORKSPACE'],
                                        self.geoserver_config.default['DMA_CODES'])


if __name__ == '__main__':
    importer = Downloader()
    if len(argv) > 1:
        function_name = argv[1]
        function = getattr(importer, function_name, None)
        if function:
            # If the function exists, call it
            function()
        else:
            print(f"Function '{function_name}' not found.")
    else:
        # If no arguments are provided, default to running the geoserver_get_map
        importer.geoserver_get_map()
