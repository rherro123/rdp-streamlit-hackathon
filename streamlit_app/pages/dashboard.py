import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st
import sys
import os
import threading, time
import random
from pages.alerts import flag_hot_sku
from db import get_all_data, WarehouseData
import os
from datetime import datetime

def main():
    data = get_all_data()
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
                        
            data.dock_status.loc[random_index, 'Days of Service'] = random.randint(1, 20)
            data.dock_status.loc[random_index, 'Last Refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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

main()
