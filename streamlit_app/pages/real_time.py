import time, threading
import sqlite3
import pandas as pd
import Warehouse_Data as wd

if __name__ == "__main__":
    conn = sqlite3.connect('warehouse_data.db')
    cursor = conn.cursor()

    data = wd.WarehouseData()

    #Starts the heart beat to refresh data every interval_seconds
    def start_data_heartbeat(interval_seconds=5):
        def refresher():
            conn_ref = sqlite3.connect('warehouse_data.db')
            while True:
                time.sleep(interval_seconds)
                print("Refreshing data...")
                alerts_df = pd.read_sql_query('SELECT * FROM alerts;', conn_ref)

                skus_df = pd.read_sql('SELECT * FROM skus WHERE sku_id IN (SELECT sku_id FROM alerts);', conn_ref)
                
                dock_status_df = pd.read_sql('SELECT * FROM dock_status', conn_ref)

                skus_all_df = pd.read_sql('SELECT * FROM skus;', conn_ref)
                production_pipeline_df = pd.read_sql('SELECT * FROM production_pipeline', conn_ref)
                

                #Update the data object with all fresh data
                data.alerts = alerts_df
                data.skus = skus_df
                data.dock_status = dock_status_df
                data.skus_all = skus_all_df
                data.production_pipeline = production_pipeline_df

                return data
        #Create the thread that'll refresh data
        thread = threading.Thread(target=refresher, daemon=True)
        thread.start()

    #Start the heartbeat
    start_data_heartbeat()
    time.sleep(5)
