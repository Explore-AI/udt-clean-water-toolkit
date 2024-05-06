import os
import sys
from os import environ, makedirs
from os.path import exists, join
import psycopg2
from geo.Geoserver import Geoserver
from requests import get, put, post, exceptions
from requests.auth import HTTPBasicAuth
from random import randint


class GeoServerAuth:
    def __init__(self, geoserver_site_url, username, password):
        self.geo = Geoserver(geoserver_site_url, username=username, password=password)
        self.auth = HTTPBasicAuth(username, password)


class Importer:
    def __init__(self):
        self.default = {
            'GEO_USER': environ.get('GEOSERVER_ADMIN_USER', 'admin'),
            'GEO_PASS': environ.get('GEOSERVER_ADMIN_PASSWORD'),
            'GEO_WORKSPACE': environ.get('GEOSERVER_WORKSPACE', 'udt'),
            'GEOSERVER_INSTANCE_URL': environ.get('GEOSERVER_URL', 'http://localhost:8080/geoserver'),
            'DATABASE_HOST': environ.get('HOST', 'udtpostgis'),
            'DATABASE_USER': environ.get('POSTGRES_USER', 'udt'),
            'DATABASE_PASSWORD': environ.get('POSTGRES_PASS'),
            'DATABASE_NAME': environ.get('POSTGRES_DB', 'udt'),
            'GEOSERVER_DATA_DIR': environ.get('GEOSERVER_DATA_DIR', '/opt/geoserver/data_dir')

        }
        # Initialize GeoServerAuth instance
        self.geoserver_auth = GeoServerAuth(
            self.default['GEOSERVER_INSTANCE_URL'],
            self.default['GEO_USER'],
            self.default['GEO_PASS']
        )

    # Function to create a workspace in GeoServer
    def publish_workspace(self, geoserver_site_url, workspace_name):
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

    # Function to retrieve spatial tables from PostgreSQL
    def pg_connection_details(self, pg_host, pg_user, pg_pass, pg_name):
        try:
            connection = psycopg2.connect(host='%s' % pg_host, database='%s' % pg_name,
                                          user='%s' % pg_user, password='%s' % pg_pass,
                                          port=5432)
            cursor = connection.cursor()
            _extension_loaded = "SELECT extname FROM pg_extension where extname = 'postgis';"
            cursor.execute(_extension_loaded)
            extension_loaded = cursor.fetchone()
            _tables = []  # Define _tables as an empty list
            if extension_loaded:
                check_table = '''SELECT f_table_name,type from geometry_columns WHERE f_table_schema = 'public';'''
                cursor.execute(check_table)
                _tables = [row for row in cursor.fetchall()]
            cursor.close()
            connection.close()
        except psycopg2.OperationalError:
            sys.exit(1)
        return _tables

    def generate_random_color(self):
        return '#{:06x}'.format(randint(0, 0xFFFFFF))

    def generate_layer_style(self, geom_type, layer_name, data_path):
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
        else:
            print(f"Layer SLD file {layer_sld} already exists. Skipping writing to it.")
        layer_sld = layer_sld.lstrip('\n')
        return layer_sld

    # Function to publish vector data as GeoServer layers
    def publish_layer_stores(self, geoserver_site_url, workspace_name, pg_host, pg_user, pg_pass,
                             pg_name, data_path):
        geo = self.geoserver_auth.geo
        auth = self.geoserver_auth.auth

        pg_tables = self.pg_connection_details(pg_host, pg_user, pg_pass, pg_name)

        if pg_tables:
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
                    style_params = self.generate_layer_style(geom_type, table, data_path)
                    style_path = join(data_path, 'styles')
                    os.chdir(style_path)
                    style_rest_url = geoserver_site_url + '/rest/styles'
                    payload = f"<style><name>{table}</name><filename>{table}.sld</filename></style>"
                    headers = {
                        "Content-type": "text/xml"
                    }
                    auth = self.geoserver_auth.auth

                    response = post(style_rest_url, headers=headers, data=payload, auth=auth)
                    if response.ok:
                        geo.publish_style(layer_name='%s' % table, style_name='%s' % table,
                                          workspace='%s' % workspace_name)
                    else:
                        print(f"Failed to create style. Status code: {response.status_code}")

    # Function to update bounding box of layer
    def recalculate_bbox(self, geo_site_url, workspace_name, pg_host, pg_user, pg_pass, pg_name):
        auth = self.geoserver_auth.auth
        headers = {"Content-type": "text/xml"}
        xml_data = "<featureType><enabled>true</enabled></featureType>"
        _tables = self.pg_connection_details(pg_host, pg_user, pg_pass, pg_name)
        if _tables:
            for table, geom_type in _tables:
                rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s?recalculate=nativebbox,latlonbbox' % (
                    geo_site_url, workspace_name, workspace_name, table)
                response = put(rest_url, headers=headers, data=xml_data, auth=auth)
                if response.status_code != 200:
                    return response.raise_for_status()

    def geoserver_requests(self):
        # Create geoserver workspace and set it as a default one
        self.publish_workspace(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_WORKSPACE'])

        # Create Database store connecting to PostgreSQL database
        self.publish_store(self.default['GEOSERVER_INSTANCE_URL'],
                           self.default['GEO_WORKSPACE'], self.default['DATABASE_HOST'],
                           self.default['DATABASE_USER'],
                           self.default['DATABASE_PASSWORD'], self.default['DATABASE_NAME'])

        # Publish layers from database to GeoServer with default styles

        self.publish_layer_stores(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_WORKSPACE'],
                                  self.default['DATABASE_HOST'],
                                  self.default['DATABASE_USER'],
                                  self.default['DATABASE_PASSWORD'],
                                  self.default['DATABASE_NAME'],
                                  self.default['GEOSERVER_DATA_DIR'])

        # Recalculate layer bounds in GeoServer layers in case the data has changed
        self.recalculate_bbox(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_WORKSPACE'],
                              self.default['DATABASE_HOST'],
                              self.default['DATABASE_USER'],
                              self.default['DATABASE_PASSWORD'], self.default['DATABASE_NAME'])


if __name__ == '__main__':
    importer = Importer()
    importer.geoserver_requests()
