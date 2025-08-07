import pandas as pd

class WarehouseData:
    def __init__(self, alerts: pd.DataFrame=None, skus:pd.DataFrame=None, dock_status:pd.DataFrame=None, skus_all:pd.DataFrame=None, production_pipeline:pd.Dataframe=None):
        self.alerts = alerts
        self.skus = skus
        self.dock_status = dock_status
        self.skus_all = skus_all
        self.production_pipeline = production_pipeline
