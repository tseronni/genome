import sys
import os
import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Paths:
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Paths, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        if not self._initialized:
            self._initialized = True

            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                self.root_dir = os.path.normpath(sys._MEIPASS)
                self.program_directory = os.path.normpath(os.path.dirname(os.path.abspath(sys.executable)))
                print('running in a PyInstaller exe bundle')
            else:
                self.root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir + os.sep + os.pardir)
                self.program_directory = self.root_dir

            self.data_raw = os.path.join(self.root_dir, os.path.join('data', 'raw'))
            self.data_processed = os.path.join(self.root_dir, os.path.join('data', 'processed'))
            self.data_external = os.path.join(self.root_dir, os.path.join('data', 'external'))

            # RAW DATA PATHS
            self.raw_abstract = os.path.join(self.data_raw, 'abstract.csv')
            self.raw_list_of_companies = os.path.join(self.data_raw, 'ListOfCompanies.csv')
            self.raw_raw_patents = os.path.join(self.data_raw, 'raw_patents.csv')
            self.raw_table_for_applicants = os.path.join(self.data_raw, 'table_for_applicants.csv')
            self.raw_ipc_titles = os.path.join(self.data_raw, 'IPC Titles.xlsx')
            self.raw_cities_500 = os.path.join(self.data_raw, 'cities500.txt')

            # RAW PARQUET DATA PATHS
            self.raw_parquet_abstract = os.path.join(self.data_raw, 'abstract.parquet')
            self.raw_parquet_list_of_companies = os.path.join(self.data_raw, 'ListOfCompanies.parquet')
            self.raw_parquet_raw_patents = os.path.join(self.data_raw, 'raw_patents.parquet')
            self.raw_parquet_table_for_applicants = os.path.join(self.data_raw, 'table_for_applicants.parquet')

            self.processed_cities_500 = os.path.join(self.data_processed, 'cities500.csv')

            # CREATE PARQUET IF NOT EXIST
            if not os.path.exists(self.raw_parquet_abstract):
                logging.info('Creating abstract.parquet...')
                df = pd.read_csv(self.raw_abstract, encoding='utf-8')
                df.to_parquet(self.raw_parquet_abstract)

            if not os.path.exists(self.raw_parquet_list_of_companies):
                logging.info('Creating ListOfCompanies.parquet...')
                df = pd.read_csv(self.raw_list_of_companies, encoding='utf-8')
                df.to_parquet(self.raw_parquet_list_of_companies)

            if not os.path.exists(self.raw_parquet_raw_patents):
                logging.info('Creating raw_patents.parquet...')
                df = pd.read_csv(self.raw_raw_patents, encoding='utf-8')
                df.to_parquet(self.raw_parquet_raw_patents)

            if not os.path.exists(self.raw_parquet_table_for_applicants):
                logging.info('Creating table_for_applicants.parquet...')
                df = pd.read_csv(self.raw_table_for_applicants, encoding='utf-8')
                df.to_parquet(self.raw_parquet_table_for_applicants)

            if not os.path.exists(self.processed_cities_500):

                if not os.path.exists(self.raw_cities_500):
                    logging.error('cities500.txt not found. Download the cities zip from http://download.geonames.org/export/dump/cities500.zip and extract content to data\raw folder')
                else:
                    logging.info('Creating cities500.csv')
                    # http://download.geonames.org/export/dump/readme.txt
                    # http://download.geonames.org/export/dump/cities500.zip

                    column_names = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
                                    'feature class', 'feature code', 'country code', 'cc2', 'admin1 code', 'admin2 code', 'admin3 code',
                                    'admin4 code', 'population', 'elevation', 'dem', 'timezone', 'modification date']

                    df_cities_500 = pd.read_csv(self.raw_cities_500, sep='\t', encoding='utf-8', names=column_names, header=0, dtype={13: str, 14: str})
                    df_cities_500.to_csv(self.processed_cities_500, index=False)
