from Models.Battery import Battery
import pandas as pd


class SimulationResult:

    def __init__(self, battery: Battery):
            
        # COLUMN_NAMES = ['Uhrzeit', 'PV [kW]', 'Verbrauch [kW]', 'Leistungsüberschüss [kW]','Battery Kapazität [kWh]',
        # 'Battery Leistungsdurchsatz [kW]', 'Battery Betrieb Verbrauch [kW]', 'Battery Betrieb Energie [kWh]' ]
        self.df = pd.DataFrame()
        self.battery = battery
        self.resolution = battery.Resolution
    
    def add_new_row(self,row: pd.DataFrame):
        self.df = pd.concat([row,self.df.loc[:]]).reset_index(drop=True)