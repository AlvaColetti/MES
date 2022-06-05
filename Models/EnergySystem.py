from pandas import DataFrame
import pandas as pd
from Models.Consumer import Consumer
from Models.Battery import Battery
from Models.PVSystem import PVSystem


class EnergySystem:
    
    def __init__(self, consumer: Consumer, battery: Battery, pvSystem: PVSystem):
        self.loadProfile = consumer
        self.pvSystem = pvSystem
        self.battery = battery
        self.checkDataFrames()

        column_names = ['Uhrzeit', 'PV [kW]', 'Verbrauch [kW]', 'Leistungsüberschüss [kW]','Battery Kapazität [kWh]',
        'Battery Leistungsdurchsatz [kW]', 'Battery Betrieb Verbrauch [kW]', 'Battery Betrieb Energie [kWh]' ]
        self.dfSimulationResult = DataFrame(columns=column_names)
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
    
    def simulate(self):
        for i in range(0,self.loadProfile.get_profile_count()-1):

            uhrzeit = self.loadProfile.profile.loc[i,"Uhrzeit"]
            consumption = self.loadProfile.profile.loc[i,"Leistung"]
            generation = self.pvSystem.profile.loc[i,"Leistung"]
            demandedPower = float(generation)-float(consumption)
            
            self.battery.simulate_responde(demandedPower)
            
            new_row = pd.DataFrame({'Uhrzeit': uhrzeit, 'PV [kW]': generation, 'Verbrauch [kW]': consumption,
             'Leistungsüberschüss [kW]': demandedPower, 'Battery Kapazität [kWh]': self.battery.state,
             'Battery Leistungsdurchsatz [kW]' : self.battery.powerThrouhput, 
             'Battery Betrieb Verbrauch [kW]' : self.battery.operation_consumption,
             'Battery Betrieb Energie [kWh]' :self.battery.operation_energy},
              index = [0])
            
            self.dfSimulationResult = pd.concat([new_row,self.dfSimulationResult.loc[:]]).reset_index(drop=True)

    def checkDataFrames(self):
        if self.loadProfile.get_profile_count() != self.pvSystem.get_profile_count():
            raise Exception("The data frames do not have the same length")