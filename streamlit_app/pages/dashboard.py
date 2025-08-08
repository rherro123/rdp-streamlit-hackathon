import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st
import sys
import os
import threading, time
import random
from pages.alerts import flag_hot_sku
    
class WarehouseData:
    def __init__(self, alerts: pd.DataFrame=None, skus:pd.DataFrame=None, dock_status:pd.DataFrame=None, skus_all:pd.DataFrame=None, production_pipeline:pd.DataFrame=None):
        self.alerts = alerts
        self.skus = skus
        self.dock_status = dock_status
        self.skus_all = skus_all
        self.production_pipeline = production_pipeline
   
def connect_to_db():
    connection = sqlite3.connect('warehouse_data.db')
    c = connection.cursor()
    return connection, c

@st.cache_data
def fetch_skus_with_alerts():
    connection, cursor = connect_to_db()
    sql = """SELECT * FROM skus WHERE sku_id IN (SELECT sku_id FROM alerts);"""
    df = pd.read_sql_query(sql, connection)
    connection.close()
    return df

def get_data():
    conn_ref, cursor = connect_to_db()
    
    alerts_df = pd.read_sql_query('SELECT * FROM alerts;', conn_ref)

    skus_df = pd.read_sql('SELECT * FROM skus WHERE sku_id IN (SELECT sku_id FROM alerts);', conn_ref)
    
    dock_status_df = pd.read_sql('SELECT d.*, s.product_name, s.product_number, s.destination, s.remortgage_gallons, s.pallets, s.weight_lbs FROM dock_status as d INNER JOIN skus as s ON d.sku_id = s.sku_id', conn_ref)

    skus_all_df = pd.read_sql('SELECT * FROM skus;', conn_ref)
    production_pipeline_df = pd.read_sql('SELECT * FROM production_pipeline', conn_ref)    
    data = WarehouseData(alerts_df, skus_df, dock_status_df, skus_all_df, production_pipeline_df)
    
    return data
    
                
def main():
    connection, cursor = connect_to_db()

    data = get_data()
    
    st.set_page_config(
        page_title="Real-time Dock Status Dashboard",
        page_icon="✅",
        layout="wide",
    )
    
    st.title("Dock Status Dashboard")  

    placeholder = st.empty()
   
    # real-time data simulation happens in this while loop
    while True:
        with placeholder.container():
            
            ### THIS SECTION JUST RANDOMIZES DAYS OF SERVICE VALUE
            random_row = data.dock_status.sample(n=1)
            random_index = random_row.index[0]
                        
            data.dock_status.loc[random_index, 'days_of_service'] = random.randint(1, 20)
            
            
            flagged_skus_df = data.dock_status.style.apply(flag_hot_sku, axis=1)    
            
            st.markdown('### Alerts')
            st.dataframe(data.alerts)
            st.markdown('### SKUs')
            st.dataframe(data.skus)
            st.markdown('### Dock Status')
            st.dataframe(flagged_skus_df)
            st.markdown('### Production Pipeline')
            st.dataframe(data.production_pipeline)
            st.markdown('### SKUs All')
            st.dataframe(data.skus_all)
            time.sleep(2)
    
        connection.close()

main()
