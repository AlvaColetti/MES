from models.battery import Battery
import pandas as pd


class SimulationResult:

    def __init__(self, battery: Battery):
        self.df = pd.DataFrame()
        self.battery = battery
        self.resolution = battery.Resolution
    
    def add_new_row(self,row: pd.DataFrame):
        self.df = pd.concat([row,self.df.loc[:]]).reset_index(drop=True)