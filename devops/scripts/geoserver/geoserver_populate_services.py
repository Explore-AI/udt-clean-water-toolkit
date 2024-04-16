import sys
from os import environ
import psycopg2
from geo.Geoserver import Geoserver
from requests import get, put, exceptions
from requests.auth import HTTPBasicAuth


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
            'DATABASE_NAME': environ.get('POSTGRES_DB', 'udt')

        }
    # Function to create a workspace in GeoServer
    def publish_workspace(self, geoserver_site_url, username, user_pass, workspace_name):
        geo = Geoserver(geoserver_site_url, username='%s' % username, password='%s' % user_pass)

        auth = HTTPBasicAuth('%s' % username, '%s' % user_pass)
        try:
            rest_url = '%s/rest/workspaces/%s.json' % (geoserver_site_url, workspace_name)
            response = get(rest_url, auth=auth)
            response.raise_for_status()
        except exceptions.HTTPError:
            geo.create_workspace(workspace='%s' % workspace_name)
            geo.set_default_workspace('%s' % workspace_name)

    # Function to create a store in GeoServer
    def publish_store(self, geoserver_site_url, username, user_pass, workspace_name, pg_host, pg_user, pg_pass,
                      pg_name):
        geo = Geoserver(geoserver_site_url, username='%s' % username, password='%s' % user_pass)
        auth = HTTPBasicAuth('%s' % username, '%s' % user_pass)
        try:
            rest_url = '%s/rest/workspaces/%s/datastores/%s.json' % (geoserver_site_url, workspace_name, workspace_name)
            response = get(rest_url, auth=auth)
            response.raise_for_status()
        except exceptions.HTTPError:
            geo.create_featurestore(store_name='%s' % workspace_name, workspace='%s' % workspace_name,
                                    db='%s' % pg_name,
                                    host='%s' % pg_host,
                                    pg_user='%s' % pg_user, pg_password='%s' % pg_pass)

    # Function to retrieve spatial tables in PostgreSQL
    def pg_connection_details(self, pg_host, pg_user, pg_pass, pg_name):
        try:

            connection = psycopg2.connect(host='%s' % pg_host, database='%s' % pg_name,
                                          user='%s' % pg_user, password='%s' % pg_pass,
                                          port=5432)
            cursor = connection.cursor()
            check_table = '''SELECT f_table_name from geometry_columns WHERE f_table_schema = 'public';'''
            cursor.execute(check_table)
            _tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            connection.close()
        except psycopg2.OperationalError:
            sys.exit(1)
        return _tables

    # Function to publish vector data as GeoServer layers
    def publish_layer_stores(self, geoserver_site_url, username, user_pass, workspace_name, pg_host, pg_user, pg_pass,
                             pg_name):
        geo = Geoserver(geoserver_site_url, username='%s' % username, password='%s' % user_pass)
        auth = HTTPBasicAuth('%s' % username, '%s' % user_pass)

        pg_tables = self.pg_connection_details(pg_host, pg_user, pg_pass, pg_name)

        for table in pg_tables:
            try:
                rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s.json' % (
                    geoserver_site_url, workspace_name, workspace_name, table)
                response = get(rest_url, auth=auth)
                print(response.raise_for_status())
                response.raise_for_status()
            except exceptions.HTTPError:
                geo.publish_featurestore(workspace='%s'
                                                   % workspace_name, store_name='%s' % workspace_name,
                                         pg_table='%s' % table)

    # Function to update bounding box of layer
    def recalculate_bbox(self, geo_site_url, username, user_pass, workspace_name, pg_host, pg_user, pg_pass, pg_name):
        auth = HTTPBasicAuth('%s' % username, '%s' % user_pass)
        headers = {"Content-type": "text/xml"}
        xml_data = "<featureType><enabled>true</enabled></featureType>"
        _tables = self.pg_connection_details(pg_host, pg_user, pg_pass, pg_name)
        for table in _tables:
            rest_url = '%s/rest/workspaces/%s/datastores/%s/featuretypes/%s?recalculate=nativebbox,latlonbbox' % (
                geo_site_url, workspace_name, workspace_name, table)
            response = put(rest_url, headers=headers, data=xml_data, auth=auth)
            if response.status_code != 200:
                return response.raise_for_status()

    def geoserver_requests(self):
        # Create geoserver workspace and set it as a default one
        self.publish_workspace(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_USER'],
                               self.default['GEO_PASS'], self.default['GEO_WORKSPACE'])

        # Create Database store connecting to PostgreSQL database
        self.publish_store(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_USER'], self.default['GEO_PASS'],
                           self.default['GEO_WORKSPACE'], self.default['DATABASE_HOST'],
                           self.default['DATABASE_USER'],
                           self.default['DATABASE_PASSWORD'], self.default['DATABASE_NAME'])

        # Publish layers from database to GeoServer with default styles

        self.publish_layer_stores(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_USER'],
                                  self.default['GEO_PASS'], self.default['GEO_WORKSPACE'],
                                  self.default['DATABASE_HOST'],
                                  self.default['DATABASE_USER'],
                                  self.default['DATABASE_PASSWORD'],
                                  self.default['DATABASE_NAME'])

        # Recalculate layer bounds in GeoServer layers in case the data has changed
        self.recalculate_bbox(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_USER'],
                              self.default['GEO_PASS'], self.default['GEO_WORKSPACE'],
                              self.default['DATABASE_HOST'],
                              self.default['DATABASE_USER'],
                              self.default['DATABASE_PASSWORD'], self.default['DATABASE_NAME'])


if __name__ == '__main__':
    importer = Importer()
    importer.geoserver_requests()