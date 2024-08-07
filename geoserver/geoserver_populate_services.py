from os import makedirs
from os.path import exists, join
from random import randint
from requests import get, put, exceptions, post, delete
from utils.utils import GeoServerConfig, DBConnection
from sys import argv


class Importer:
    def __init__(self):
        self.geoserver_config = GeoServerConfig()
        self.geoserver_auth = self.geoserver_config.geoserver_auth

    def publish_gwc_grid(self, geoserver_site_url):
        auth = self.geoserver_auth.auth
        try:
            rest_url = '%s/gwc/rest/gridsets/EPSG:3857.json' % geoserver_site_url
            response = get(rest_url, auth=auth)
            response.raise_for_status()
        except exceptions.HTTPError:

            xml = """ 
                    <gridSet>
                      <name>EPSG:3857</name>
                      <srs>
                        <number>3857</number>
                      </srs>
                      <extent>
                        <coords>
                          <double>-2.003750834E7</double>
                          <double>-2.003750834E7</double>
                          <double>2.003750834E7</double>
                          <double>2.003750834E7</double>
                        </coords>
                      </extent>
                      <alignTopLeft>false</alignTopLeft>
                      <resolutions>
                        <double>156543.03390625</double>
                        <double>78271.516953125</double>
                        <double>39135.7584765625</double>
                        <double>19567.87923828125</double>
                        <double>9783.939619140625</double>
                        <double>4891.9698095703125</double>
                        <double>2445.9849047851562</double>
                        <double>1222.9924523925781</double>
                        <double>611.4962261962891</double>
                        <double>305.74811309814453</double>
                        <double>152.87405654907226</double>
                        <double>76.43702827453613</double>
                        <double>38.218514137268066</double>
                        <double>19.109257068634033</double>
                        <double>9.554628534317017</double>
                        <double>4.777314267158508</double>
                        <double>2.388657133579254</double>
                        <double>1.194328566789627</double>
                        <double>0.5971642833948135</double>
                        <double>0.2985821416974068</double>
                        <double>0.1492910708487034</double>
                        <double>0.0746455354243517</double>
                        <double>0.0373227677121758</double>
                      </resolutions>
                      <metersPerUnit>1.0</metersPerUnit>
                      <pixelSize>2.8E-4</pixelSize>
                      <scaleNames>
                        <string>EPSG:3857:0</string>
                        <string>EPSG:3857:1</string>
                        <string>EPSG:3857:2</string>
                        <string>EPSG:3857:3</string>
                        <string>EPSG:3857:4</string>
                        <string>EPSG:3857:5</string>
                        <string>EPSG:3857:6</string>
                        <string>EPSG:3857:7</string>
                        <string>EPSG:3857:8</string>
                        <string>EPSG:3857:9</string>
                        <string>EPSG:3857:10</string>
                        <string>EPSG:3857:11</string>
                        <string>EPSG:3857:12</string>
                        <string>EPSG:3857:13</string>
                        <string>EPSG:3857:14</string>
                        <string>EPSG:3857:15</string>
                        <string>EPSG:3857:16</string>
                        <string>EPSG:3857:17</string>
                        <string>EPSG:3857:18</string>
                        <string>EPSG:3857:19</string>
                        <string>EPSG:3857:20</string>
                        <string>EPSG:3857:21</string>
                        <string>EPSG:3857:22</string>
                      </scaleNames>
                      <tileHeight>256</tileHeight>
                      <tileWidth>256</tileWidth>
                      <yCoordinateFirst>false</yCoordinateFirst>
                    </gridSet>"""
            put('%s/gwc/rest/gridsets/EPSG:3857.xml' % geoserver_site_url, auth=auth,
                headers={'Content-type': 'text/xml'},
                data=xml)

    # Function to create a workspace in GeoServer
    def publish_workspace(self, geoserver_site_url, workspace_name):
        """
        Args:
            geoserver_site_url: i.e. https://geoserver
            workspace_name: i.e. udt

        Returns:
            GeoServer workspace object name corresponding to workspace_name

        """
        geo = self.geoserver_auth.geo
        auth = self.geoserver_auth.auth
        try:
            rest_url = '%s/rest/workspaces/%s.json' % (geoserver_site_url, workspace_name)
            response = get(rest_url, auth=auth)
            response.raise_for_status()
        except exceptions.HTTPError:
            geo.create_workspace(workspace='%s' % workspace_name)
            geo.set_default_workspace('%s' % workspace_name)

    # Function to create a store in GeoServer
    def publish_store(self, geoserver_site_url, workspace_name, pg_host, pg_user, pg_pass,
                      pg_name):
        """
        Args:
            geoserver_site_url:
            workspace_name:
            pg_host:
            pg_user:
            pg_pass:
            pg_name:

        Returns: GeoServer store connecting to PostgreSQL database

        """
        geo = self.geoserver_auth.geo
        auth = self.geoserver_auth.auth

        try:
            rest_url = '%s/rest/workspaces/%s/datastores/%s.json' % (geoserver_site_url, workspace_name, workspace_name)
            response = get(rest_url, auth=auth)
            response.raise_for_status()
        except exceptions.HTTPError:
            geo.create_featurestore(store_name='%s' % workspace_name, workspace='%s' % workspace_name,
                                    db='%s' % pg_name,
                                    host='%s' % pg_host,
                                    pg_user='%s' % pg_user, pg_password='%s' % pg_pass)

    def generate_random_color(self):
        return '#{:06x}'.format(randint(0, 0xFFFFFF))

    def generate_layer_style(self, geom_type, layer_name, data_path):
        """
        Generate a random layer style based on the geom_type and layer_name, storing it in a given path
        Args:
            geom_type:
            layer_name:
            data_path:

        Returns: SLD document for each layer resource

        """
        std_color = self.generate_random_color()
        if 'POLYGON' in geom_type:
            sld_xml = f'''
                <PolygonSymbolizer>
                <Fill>
                  <CssParameter name="fill">{std_color}</CssParameter>
                </Fill>
                <Stroke>
                  <CssParameter name="stroke">{std_color}</CssParameter>
                  <CssParameter name="stroke-width">1</CssParameter>
                </Stroke>
              </PolygonSymbolizer>
                '''
        elif 'POINT' in geom_type:
            sld_xml = f'''
                <PointSymbolizer>
                    <Graphic>
                        <Mark>
                            <WellKnownName>circle</WellKnownName>
                            <Fill>
                                <CssParameter name="fill">{std_color}</CssParameter>
                            </Fill>
                        </Mark>
                        <Size>6</Size>
                    </Graphic>
                </PointSymbolizer>
                '''
        else:
            sld_xml = f''' 
                <LineSymbolizer>
                    <Stroke>
                        <CssParameter name="stroke">{std_color}</CssParameter>
                    </Stroke>
                </LineSymbolizer>
                '''
        base_sld_xml = f'''
<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>{layer_name}</Name>
    <UserStyle>
      <FeatureTypeStyle>
        <Rule>
          <Name>{layer_name}</Name>
            {sld_xml}
        </Rule>
        </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
            '''
        sld_path = join(data_path, "styles")
        if not exists(sld_path):
            makedirs(sld_path)

        layer_sld = join(sld_path, f"{layer_name}.sld")
        if not exists(layer_sld):
            with open(layer_sld, 'w') as file:
                file.write(base_sld_xml)
                # Read the written contents from the file
            with open(layer_sld, 'r') as content:
                data = content.read().splitlines(True)
            with open(layer_sld, 'w') as formatted:
                formatted.writelines(data[1:])
        layer_sld = layer_sld.lstrip('\n')
        return layer_sld

    # Function to publish vector data as GeoServer layers
    def publish_layer_stores(self, geoserver_site_url, workspace_name, data_path):
        """
        Publish all vector layers in a PostgreSQL database.
        Args:
            geoserver_site_url:
            workspace_name:
            data_path:

        Returns: GeoServer layers with some default styles assigned

        """
        geo = self.geoserver_auth.geo
        auth = self.geoserver_auth.auth
        db_conn = DBConnection()
        pg_tables = db_conn.pg_spatial_tables()

        geoserver_feature_type_url = f"{geoserver_site_url}/rest/workspaces/{workspace_name}/featuretypes.json"
        response = get(geoserver_feature_type_url, auth=auth)
        data = response.json()
        feature_type_names = [feature_type["name"] for feature_type in data["featureTypes"]["featureType"]]

        if pg_tables:
            # Cleanup GeoServer tables if DB config has changed
            for feature_type in feature_type_names:
                if feature_type not in pg_tables:
                    # Delete the layer from GeoServer
                    layer_url = f"{geoserver_site_url}/rest/layers/{workspace_name}:{feature_type}?recurse=true"
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    }
                    response = delete(layer_url, headers=headers, auth=auth)
                    if response.status_code == 200:
                        print(f"Deleted layer: {workspace_name}:{feature_type}")
                    else:
                        print(f"Error deleting layer: {workspace_name}:{feature_type}")
            for table, geom_type in pg_tables:
                try:
                    rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s.json' % (
                        geoserver_site_url, workspace_name, workspace_name, table)
                    response = get(rest_url, auth=auth)
                    response.raise_for_status()
                except exceptions.HTTPError:
                    geo.publish_featurestore(workspace='%s'
                                                       % workspace_name, store_name='%s' % workspace_name,
                                             pg_table='%s' % table)
                    # Add checks to see if SLD exists
                    layer_sld_file = self.generate_layer_style(geom_type, table, data_path)
                    response = geo.upload_style(path=r'%s' % layer_sld_file, workspace='%s' % workspace_name)

                    if response == 200:
                        geo.publish_style(layer_name='%s' % table, style_name='%s' % table,
                                          workspace='%s' % workspace_name)
                        # Update layer configuration for gwc
                        layer_xml = """
                                    <GeoServerLayer>
                                      <enabled>true</enabled>
                                      <inMemoryCached>true</inMemoryCached>
                                      <name>{geo_workspace}:{geo_layer}</name>
                                      <mimeFormats>
                                        <string>application/vnd.mapbox-vector-tile</string>
                                        <string>image/png</string>
                                        <string>image/jpeg</string>
                                      </mimeFormats>
                                      <gridSubsets>
                                        <gridSubset>
                                          <gridSetName>EPSG:900913</gridSetName>
                                          <extent>
                                            <coords>
                                              <double>-871762.9336153703</double>
                                              <double>6406067.029592626</double>
                                              <double>40978.26046182055</double>
                                              <double>6827410.395957927</double>
                                            </coords>
                                          </extent>
                                        </gridSubset>
                                        <gridSubset>
                                          <gridSetName>EPSG:3857</gridSetName>
                                        </gridSubset>
                                        <gridSubset>
                                          <gridSetName>EPSG:4326</gridSetName>
                                          <extent>
                                            <coords>
                                              <double>-7.831179673955589</double>
                                              <double>49.76726301031473</double>
                                              <double>0.3681139768948408</double>
                                              <double>52.15064734867595</double>
                                            </coords>
                                          </extent>
                                        </gridSubset>
                                      </gridSubsets>
                                      <metaWidthHeight>
                                        <int>4</int>
                                        <int>4</int>
                                      </metaWidthHeight>
                                      <expireCache>0</expireCache>
                                      <expireClients>0</expireClients>
                                      <parameterFilters>
                                        <styleParameterFilter>
                                          <key>STYLES</key>
                                          <defaultValue></defaultValue>
                                        </styleParameterFilter>
                                      </parameterFilters>
                                      <gutter>0</gutter>
                                      <cacheWarningSkips/>
                                    </GeoServerLayer>
                                    """.format(geo_workspace=workspace_name, geo_layer=table)
                        post('%s/gwc/rest/layers/%s:%s.xml' % (geoserver_site_url, workspace_name, table), auth=auth,
                             headers={'Content-type': 'text/xml'}, data=layer_xml)
                    else:
                        print(f"Failed to create style. Status code: {response.status_code}")

    def update_layer_stores(self, geoserver_site_url, workspace_name, data_path):
        """
        Republish all vector layers in a PostgreSQL database.
        Args:
            geoserver_site_url:
            workspace_name:
            data_path:

        Returns: GeoServer layers with some default styles assigned

        """
        geo = self.geoserver_auth.geo
        auth = self.geoserver_auth.auth
        db_conn = DBConnection()
        pg_tables = db_conn.pg_spatial_tables()

        if pg_tables:
            for table, geom_type in pg_tables:
                rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s.json' % (
                    geoserver_site_url, workspace_name, workspace_name, table)
                response = get(rest_url, auth=auth)
                response.raise_for_status()
                if response.status_code == 200:
                    geo.delete_layer(layer_name='%s' % table, workspace='%s' % workspace_name)
                    geo.publish_featurestore(workspace='%s'
                                                       % workspace_name, store_name='%s' % workspace_name,
                                             pg_table='%s' % table)
                    geo.publish_style(layer_name='%s' % table, style_name='%s' % table,
                                      workspace='%s' % workspace_name)

                else:
                    print(f"Failed to delete layers. Status code: {response.status_code}")

    # Function to update bounding box of layer
    def recalculate_bbox(self, geo_site_url, workspace_name):
        """
        Recalculate the bounding box of published resources if the data has been updated in the database
        Args:
            geo_site_url:
            workspace_name:

        Returns:

        """
        auth = self.geoserver_auth.auth
        headers = {"Content-type": "text/xml"}
        xml_data = "<featureType><enabled>true</enabled></featureType>"
        db_conn = DBConnection()
        _tables = db_conn.pg_extent_details()
        if _tables:
            for table, geom_type in _tables:
                rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s?recalculate=nativebbox,latlonbbox' % (
                    geo_site_url, workspace_name, workspace_name, table)
                response = put(rest_url, headers=headers, data=xml_data, auth=auth)
                if response.status_code != 200:
                    return response.raise_for_status()

    def seed_all_layers(self, geo_site_url, workspace_name, grid_srs, layer_list=None):
        auth = self.geoserver_auth.auth
        db_conn = DBConnection()
        published_tables = db_conn.pg_spatial_tables()
        layer_lists = published_tables if layer_list is None else layer_list
        if layer_lists:
            for table, geom_type in layer_lists:
                url = "%s/gwc/rest/seed/%s:%s.xml" % (geo_site_url, workspace_name, table)
                payload = '<seedRequest><name>%s:%s</name><srs><number>%s</number></srs><zoomStart>1</zoomStart><zoomStop>12</zoomStop><format>application/vnd.mapbox-vector-tile</format><type>truncate</type><threadCount>4</threadCount></seedRequest>' % (
                    workspace_name, table, grid_srs)
                headers = {'Content-Type': 'text/xml'}
                response = post(url, headers=headers, data=payload, auth=auth)
                if response.status_code != 200:
                    return response.raise_for_status()

    def truncate_all_layers(self, geo_site_url, workspace_name, grid_srs, layer_list=None):
        auth = self.geoserver_auth.auth
        db_conn = DBConnection()
        db_tables = db_conn.pg_extent_details()
        layer_lists = db_tables if layer_list is None else layer_list
        if layer_lists:
            for table_name, bbox in layer_lists:
                url = "{}/gwc/rest/seed/{}:{}.json".format(geo_site_url, workspace_name, table_name)
                name = "{}:{}".format(workspace_name, table_name)
                coords = {"double": [str(coord) for coord in bbox]}
                auth_name = "EPSG"
                srs = "{}:{}".format(auth_name, grid_srs)

                payload = {
                    "seedRequest": {
                        "name": name,
                        "bounds": {
                            "coords": coords
                        },
                        "srs": srs,
                        "zoomStart": 1,
                        "zoomStop": 12,
                        "format": "application/vnd.mapbox-vector-tile",
                        "type": "truncate",
                        "threadCount": 4
                    }
                }

                response = post(url, json=payload, auth=auth)
                if response.status_code != 200:
                    return response.raise_for_status()

    def populate_geoserver(self):
        """
        Procedure to automate the geoserver requests so that we can be able to view the OGC services
        Returns:

        """
        # Add a grid to GeoServer
        self.publish_gwc_grid(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'])
        # Create geoserver workspace and set it as a default one
        self.publish_workspace(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                               self.geoserver_config.default['GEO_WORKSPACE'])

        # Create Database store connecting to PostgreSQL database
        self.publish_store(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                           self.geoserver_config.default['GEO_WORKSPACE'],
                           self.geoserver_config.default['DATABASE_HOST'],
                           self.geoserver_config.default['DATABASE_USER'],
                           self.geoserver_config.default['DATABASE_PASSWORD'],
                           self.geoserver_config.default['DATABASE_NAME'])

        # Publish layers from database to GeoServer with default styles

        self.publish_layer_stores(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                                  self.geoserver_config.default['GEO_WORKSPACE'],
                                  self.geoserver_config.default['GEOSERVER_DATA_DIR'])
        # Fix lat long bounds
        self.recalculate_bbox(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                              self.geoserver_config.default['GEO_WORKSPACE'])

    # Cache all layers
    def gwc_cache_all_layers(self):
        self.seed_all_layers(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                             self.geoserver_config.default['GEO_WORKSPACE'], self.geoserver_config.default['GWC_GRID'])

    # Cleanup layer stores
    def gwc_cache_truncate_all_layers(self):
        self.truncate_all_layers(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                                 self.geoserver_config.default['GEO_WORKSPACE'],
                                 self.geoserver_config.default['GWC_GRID'])

    # Republish layers from PostgreSQL as they have changed
    def reload_geoserver_layers(self):
        self.update_layer_stores(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                                 self.geoserver_config.default['GEO_WORKSPACE'],
                                 self.geoserver_config.default['GEOSERVER_DATA_DIR'])

    def recalculate_layer_bbox(self):
        # Recalculate layer bounds in GeoServer layers in case the data has changed
        self.recalculate_bbox(self.geoserver_config.default['GEOSERVER_INSTANCE_URL'],
                              self.geoserver_config.default['GEO_WORKSPACE'])


if __name__ == '__main__':
    importer = Importer()
    # Pass command line args
    if len(argv) > 1:
        function_name = argv[1]
        function = getattr(importer, function_name, None)
        if function:
            # If the function exists, call it
            function()
        else:
            print(f"Function '{function_name}' not found.")
    else:
        # If no arguments are provided, default to running the populate_geoserver
        importer.populate_geoserver()
