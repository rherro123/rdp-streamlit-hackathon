import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st
import sys
import os
import threading, time

class WarehouseData:
    def __init__(self, alerts: pd.DataFrame=None, skus:pd.DataFrame=None, dock_status:pd.DataFrame=None, skus_all:pd.DataFrame=None, production_pipeline:pd.DataFrame=None):
        self.alerts = alerts
        self.skus = skus
        self.dock_status = dock_status
        self.skus_all = skus_all
        self.production_pipeline = production_pipeline

data = WarehouseData()
    
def connect_to_db():
    connection = sqlite3.connect('warehouse_data.db')
    c = connection.cursor()
    return connection, c

def fetch_skus_with_alerts():
    connection, cursor = connect_to_db()
    sql = """SELECT * FROM skus WHERE sku_id IN (SELECT sku_id FROM alerts);"""
    df = pd.read_sql_query(sql, connection)
    connection.close()
    return df

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

    #Create the thread that'll refresh data
    thread = threading.Thread(target=refresher, daemon=True)
    thread.start()

            
def main():
    connection, cursor = connect_to_db()

    sku_with_alerts_df = fetch_skus_with_alerts()
    
    #start_data_heartbeat()
    #time.sleep(5)
    
    st.dataframe(sku_with_alerts_df, use_container_width=True)

    connection.close()

main()
