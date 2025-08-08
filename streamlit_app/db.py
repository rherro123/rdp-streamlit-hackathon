import sqlite3
import pandas as pd

database_file = 'warehouse_data.db'

class WarehouseData:
    def __init__(self, alerts: pd.DataFrame=None, skus:pd.DataFrame=None, dock_status:pd.DataFrame=None, skus_all:pd.DataFrame=None, production_pipeline:pd.DataFrame=None):
        self.alerts = alerts
        self.skus = skus
        self.dock_status = dock_status
        self.skus_all = skus_all
        self.production_pipeline = production_pipeline
        
def connect_to_db():
    connection = sqlite3.connect(database_file)
    c = connection.cursor()
    return connection, c

def get_all_data():
    conn_ref, cursor = connect_to_db()
    
    alerts_df = pd.read_sql_query('SELECT * FROM alerts;', conn_ref)

    skus_df = pd.read_sql('SELECT * FROM skus WHERE sku_id IN (SELECT sku_id FROM alerts);', conn_ref)
    
    dock_status_df = pd.read_sql("""SELECT 
                                s.product_number, 
                                s.product_name,
                                d.staging_lane, 
                                d.dock_location, 
                                d.last_refresh, 
                                d.days_of_service,
                                s.destination, 
                                s.remortgage_gallons, 
                                s.pallets, 
                                s.weight_lbs 
                                FROM dock_status as d INNER JOIN 
                                    skus as s ON d.sku_id = s.sku_id""", conn_ref)

    
    dock_status_df.rename(columns={'staging_lane': 'Staging Lane', 
                                   'dock_location': 'Dock Location', 
                                   'last_refresh': 'Last Refresh',
                                   'product_name': 'Product Name',
                                   'product_number': 'Product Number',
                                   'days_of_service': 'Days of Service',
                                   'destination': 'Destination',
                                   'remortgage_gallons': 'Remortgage Gallons',
                                   'pallets': 'Pallets',
                                   'weight_lbs': 'Weight (lbs)'}, inplace=True)
    
    
    skus_all_df = pd.read_sql('SELECT * FROM skus;', conn_ref)
    production_pipeline_df = pd.read_sql('SELECT * FROM production_pipeline', conn_ref)    
    data = WarehouseData(alerts_df, skus_df, dock_status_df, skus_all_df, production_pipeline_df)
    
    return data

