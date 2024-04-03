import sys
from os import environ
import psycopg2
from requests import get, put, exceptions
from requests.auth import HTTPBasicAuth


class Downloader:
    def __init__(self):
        self.default = {
            'GEO_USER': environ.get('GEOSERVER_ADMIN_USER', 'admin'),
            'GEO_PASS': environ.get('GEOSERVER_ADMIN_PASSWORD'),
            'GEO_WORKSPACE': environ.get('GEOSERVER_WORKSPACE', 'udt'),
            'GEOSERVER_INSTANCE_URL': environ.get('GEOSERVER_URL', 'http://localhost:8080/geoserver'),
            'DATABASE_HOST': environ.get('HOST'),
            'DATABASE_USER': environ.get('POSTGRES_USER'),
            'DATABASE_PASSWORD': environ.get('POSTGRES_PASS'),
            'DATABASE_NAME': environ.get('POSTGRES_DB'),
            'HEIGHT': 768,
            'WIDTH': 1024,
            'FORMAT': 'image/svg',
            'SRID': 27700

        }

    # Function to retrieve spatial tables in PostgreSQL
    def pg_connection_details(self, pg_host, pg_user, pg_pass, pg_name):
        try:
            connection = psycopg2.connect(host='%s' % pg_host, database='%s' % pg_name,
                                          user='%s' % pg_user, password='%s' % pg_pass,
                                          port=5432)
            cursor = connection.cursor()

            check_table = '''SELECT f_table_name FROM geometry_columns WHERE f_table_schema = 'public';'''
            cursor.execute(check_table)
            _tables = [row[0] for row in cursor.fetchall()]

            _tables_with_bbox = []

            for single_table in _tables:
                layer_bbox_query = '''
                    SELECT 
                        ST_XMin(ST_Extent(geometry)) AS min_x,
                        ST_YMin(ST_Extent(geometry)) AS min_y,
                        ST_XMax(ST_Extent(geometry)) AS max_x,
                        ST_YMax(ST_Extent(geometry)) AS max_y 
                    FROM 
                        public.%s;
                ''' % single_table

                cursor.execute(layer_bbox_query)
                bbox_result = cursor.fetchone()

                if bbox_result:
                    min_x, min_y, max_x, max_y = bbox_result
                    _tables_with_bbox.append((single_table, (min_x, min_y, max_x, max_y)))

            cursor.close()
            connection.close()

        except psycopg2.OperationalError:
            sys.exit(1)

        return _tables_with_bbox

    def download_and_save_image(self, url, file_path, auth=None):
        try:
            response = get(url)
            response.raise_for_status()

            with open(file_path, 'wb') as file:
                file.write(response.content)

            print("Image saved successfully:", file_path)
        except exceptions.RequestException as e:
            print("Error downloading image:", e)

    # Function to publish vector data as GeoServer layers
    def get_layer_snapshot(self, geoserver_site_url, username, user_pass, workspace_name, pg_host, pg_user, pg_pass,
                           pg_name):

        auth = HTTPBasicAuth('%s' % username, '%s' % user_pass)

        pg_tables = self.pg_connection_details(pg_host, pg_user, pg_pass, pg_name)

        for table_name, bbox in pg_tables:
            get_map_url = '%s/%s/wms?service=WMS&version=1.1.0&request=GetMap&layers=%s:%s&bbox=%s,%s,%s,%s&width=%s&height=%s&srs=EPSG:%s&styles=&format=%s' % (
                geoserver_site_url, workspace_name, workspace_name, table_name, bbox[0], bbox[1], bbox[2], bbox[3],
                self.default['HEIGHT'], self.default['WIDTH'], self.default['SRID'], self.default['FORMAT'])
            image_extension = self.default['FORMAT'].split('/')[-1]
            file_path = f"{table_name}.{image_extension}"
            # Download and save the image
            self.download_and_save_image(get_map_url, file_path, auth=auth)

    def geoserver_get_map(self):

        # Publish layers from database to GeoServer with default styles

        self.get_layer_snapshot(self.default['GEOSERVER_INSTANCE_URL'], self.default['GEO_USER'],
                                self.default['GEO_PASS'], self.default['GEO_WORKSPACE'],
                                self.default['DATABASE_HOST'],
                                self.default['DATABASE_USER'],
                                self.default['DATABASE_PASSWORD'],
                                self.default['DATABASE_NAME'])


if __name__ == '__main__':
    importer = Downloader()
    importer.geoserver_get_map()