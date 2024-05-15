from sys import exit
from psycopg2 import connect, OperationalError
from os import environ
from requests.auth import HTTPBasicAuth
from geo.Geoserver import Geoserver


class GeoServerAuth:
    def __init__(self, geoserver_site_url, username, password):
        self.geo = Geoserver(geoserver_site_url, username=username, password=password)
        self.auth = HTTPBasicAuth(username, password)


class GeoServerConfig:
    def __init__(self):
        self.default = {
            'GEO_USER': environ.get('GEOSERVER_ADMIN_USER', 'admin'),
            'GEO_PASS': environ.get('GEOSERVER_ADMIN_PASSWORD'),
            'GEO_WORKSPACE': environ.get('GEOSERVER_WORKSPACE', 'udt'),
            'GEOSERVER_INSTANCE_URL': environ.get('GEOSERVER_URL', 'http://udtgeoserver:8080/geoserver'),
            'DATABASE_HOST': environ.get('POSTGIS_DEFAULT_DB_HOST__ENV_VAR', 'udtpostgis'),
            'DATABASE_USER': environ.get('POSTGIS_DB_USER__ENV_VAR', 'udt'),
            'DATABASE_PASSWORD': environ.get('POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR'),
            'DATABASE_NAME': environ.get('POSTGIS_DB_NAME__ENV_VAR', 'udt'),
            'DATABASE_PORT': environ.get('POSTGIS_DEFAULT_PORT__ENV_VAR', 5432),
            'GEOSERVER_DATA_DIR': environ.get('GEOSERVER_DATA_DIR', '/opt/geoserver/data_dir'),
            'HEIGHT': 768,
            'WIDTH': 1024,
            'FORMAT': 'image/svg',
            'DMA_CODES': environ.get('DMA_CODES', ['ZWAL4801', 'ZCHESS12', 'ZCHIPO01'])
        }
        # Initialize GeoServerAuth instance
        self.geoserver_auth = GeoServerAuth(
            self.default['GEOSERVER_INSTANCE_URL'],
            self.default['GEO_USER'],
            self.default['GEO_PASS']
        )


class DBConnection:

    def __init__(self):
        self.conn = self.create_conn()

    def pg_extent_details(self):
        """Retrieve database connection params from PostgreSQL, returns list of tables and srid"""

        try:
            cursor = self.conn.cursor()

            _extension_loaded = "SELECT extname FROM pg_extension where extname = 'postgis';"
            cursor.execute(_extension_loaded)
            extension_loaded = cursor.fetchone()
            _tables_with_bbox = []
            if extension_loaded:
                check_table = '''SELECT f_table_name FROM geometry_columns WHERE f_table_schema = 'public';'''
                cursor.execute(check_table)
                _tables = [row[0] for row in cursor.fetchall()]
                for single_table in _tables:
                    layer_bbox_query = '''
                        SELECT 
                            ST_XMin(ST_Extent(geometry)) AS min_x,
                            ST_YMin(ST_Extent(geometry)) AS min_y,
                            ST_XMax(ST_Extent(geometry)) AS max_x,
                            ST_YMax(ST_Extent(geometry)) AS max_y ,
                            ST_SRID(geometry) as srid
                        FROM 
                            public.%s
                            GROUP BY srid;
                    ''' % single_table

                    cursor.execute(layer_bbox_query)
                    bbox_result = cursor.fetchone()

                    if bbox_result:
                        min_x, min_y, max_x, max_y, srid = bbox_result
                        _tables_with_bbox.append((single_table, (min_x, min_y, max_x, max_y, srid)))
            cursor.close()
            #self.conn.close()
        except OperationalError:
            print("Could not connect to PostgreSQL")
            exit(1)

        return _tables_with_bbox

    def pg_dma_extent_details(self, dma_codes):
        """Retrieve database connection params from PostgreSQL, returns list of tables and srid"""

        try:
            cursor = self.conn.cursor()

            _extension_loaded = "SELECT extname FROM pg_extension where extname = 'postgis';"
            cursor.execute(_extension_loaded)
            extension_loaded = cursor.fetchone()
            _tables_with_bbox = []
            if extension_loaded:
                check_dma_table = '''SELECT EXISTS(SELECT 1 FROM geometry_columns \
                WHERE f_table_schema = 'public' AND f_table_name = 'utilities_dma'); '''
                cursor.execute(check_dma_table)
                table_value = cursor.fetchone()
                if table_value:
                    if isinstance(dma_codes, list):
                        for dma in dma_codes:
                            layer_bbox_query = '''
                                SELECT 
                                    ST_XMin(ST_Extent(geometry)) AS min_x,
                                    ST_YMin(ST_Extent(geometry)) AS min_y,
                                    ST_XMax(ST_Extent(geometry)) AS max_x,
                                    ST_YMax(ST_Extent(geometry)) AS max_y ,
                                    ST_SRID(geometry) as srid
                                FROM 
                                    public."utilities_dma" where code = '%s'
                                    GROUP BY srid;
                            ''' % dma

                            cursor.execute(layer_bbox_query)
                            bbox_result = cursor.fetchone()

                            if bbox_result:
                                min_x, min_y, max_x, max_y, srid = bbox_result
                                _tables_with_bbox.append((dma, (min_x, min_y, max_x, max_y, srid)))
                    else:
                        layer_bbox_query = '''
                            SELECT 
                                ST_XMin(ST_Extent(geometry)) AS min_x,
                                ST_YMin(ST_Extent(geometry)) AS min_y,
                                ST_XMax(ST_Extent(geometry)) AS max_x,
                                ST_YMax(ST_Extent(geometry)) AS max_y ,
                                ST_SRID(geometry) as srid
                            FROM 
                                public."utilities_dma" where code = '%s'
                                GROUP BY srid;
                        ''' % dma_codes
                        cursor.execute(layer_bbox_query)
                        bbox_result = cursor.fetchone()

                        if bbox_result:
                            min_x, min_y, max_x, max_y, srid = bbox_result
                            _tables_with_bbox.append((dma_codes, (min_x, min_y, max_x, max_y, srid)))
            cursor.close()
            #self.conn.close()

        except OperationalError:
            print("Could not connect to PostgreSQL")
            exit(1)
        return _tables_with_bbox

    def pg_spatial_tables(self):
        try:
            cursor = self.conn.cursor()
            _extension_loaded = "SELECT extname FROM pg_extension where extname = 'postgis';"
            cursor.execute(_extension_loaded)
            extension_loaded = cursor.fetchone()
            _tables = []  # Define _tables as an empty list
            if extension_loaded:
                check_table = '''SELECT f_table_name,type from geometry_columns WHERE f_table_schema = 'public';'''
                cursor.execute(check_table)
                _tables = [row for row in cursor.fetchall()]
            cursor.close()
            #self.conn.close()
        except OperationalError:
            exit(1)
        return _tables

    @staticmethod
    def create_conn():
        """
        :return: psycopg2.connection
        """
        geo_server_config = GeoServerConfig()
        return connect(
            host=geo_server_config.default['DATABASE_HOST'],
            database=geo_server_config.default['DATABASE_NAME'],
            user=geo_server_config.default['DATABASE_USER'],
            password=geo_server_config.default['DATABASE_PASSWORD'],
            port=geo_server_config.default['DATABASE_PORT']
        )

    def cursor(self):
        """
        :return: psycopg2.cursor
        """
        return self.conn.cursor()

    def close_conn(self):
        """
        Close the database connection
        """
        self.conn.close()