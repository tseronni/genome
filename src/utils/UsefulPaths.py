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

            # RAW PARQUET DATA PATHS
            self.raw_parquet_abstract = os.path.join(self.data_raw, 'abstract.parquet')
            self.raw_parquet_list_of_companies = os.path.join(self.data_raw, 'ListOfCompanies.parquet')
            self.raw_parquet_raw_patents = os.path.join(self.data_raw, 'raw_patents.parquet')
            self.raw_parquet_table_for_applicants = os.path.join(self.data_raw, 'table_for_applicants.parquet')

            # CREATE PARQUET IF NOT EXIST
            if not os.path.exists(self.raw_parquet_abstract):
                logging.info('Creating abstract.parquet...')
                df = pd.read_csv(self.raw_abstract)
                df.to_parquet(self.raw_parquet_abstract)

            if not os.path.exists(self.raw_parquet_list_of_companies):
                logging.info('Creating ListOfCompanies.parquet...')
                df = pd.read_csv(self.raw_list_of_companies)
                df.to_parquet(self.raw_parquet_list_of_companies)

            if not os.path.exists(self.raw_parquet_raw_patents):
                logging.info('Creating raw_patents.parquet...')
                df = pd.read_csv(self.raw_raw_patents)
                df.to_parquet(self.raw_parquet_raw_patents)

            if not os.path.exists(self.raw_parquet_table_for_applicants):
                logging.info('Creating table_for_applicants.parquet...')
                df = pd.read_csv(self.raw_table_for_applicants)
                df.to_parquet(self.raw_parquet_table_for_applicants)
