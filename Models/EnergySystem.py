import pandas as pd
from Models.Consumer import Consumer
from Models.Battery import Battery
from Models.PVSystem import PVSystem
from Models.dependecies.SimulationResult import SimulationResult

class EnergySystem:
    
    def __init__(self, consumer: Consumer, battery: Battery, pvSystem: PVSystem):
        self.loadProfile = consumer
        self.pvSystem = pvSystem
        self.battery = battery
        self.checkDataFrames()

        self.simulation_result = SimulationResult(self.battery)
    
    def simulate(self):
        for i in range(0,self.loadProfile.get_profile_count()-1):

            uhrzeit = self.loadProfile.profile.loc[i,"Uhrzeit"]
            consumption = self.loadProfile.profile.loc[i,"Leistung"]
            generation = self.pvSystem.profile.loc[i,"Leistung"]
            demandedPower = float(generation)-float(consumption)
            
            
            self.battery.simulate_responde(demandedPower)
            battery_power = self.battery.power_throuhput
            
            new_row = pd.DataFrame({'Uhrzeit': uhrzeit, 'PV [kW]': generation, 'Verbrauch [kW]': consumption,
            'Grid use [kW]' : round(self.__calcualte_grid_use(generation, consumption, battery_power),2),
            'Consumption cover by PV [kW]' : round(self.__calculate_consumption_conver_by_pv(generation, consumption)),
            'PV feed [kW]': round(self.__calculate_pv_feed(generation, consumption, battery_power), 2),
             'Leistungsüberschüss [kW]': round(demandedPower, 2) , 'Battery Kapazität [kWh]': round(self.battery.state,5),
             'Battery Leistungsdurchsatz [kW]' : round(battery_power,2) ,
             'Battery Betrieb Verbrauch [kW]' : self.battery.current_operation_consumption,
             'Battery Betrieb Energie [kWh]' :self.battery.operation_energy},
              index = [0])
            

            if (i == 76):
                a = 0

            self.simulation_result.add_new_row(new_row)
    
        self.simulation_result.df = self.simulation_result.df.sort_values(by=['Uhrzeit'])

    def checkDataFrames(self):
        if self.loadProfile.get_profile_count() != self.pvSystem.get_profile_count():
            raise Exception("The data frames do not have the same length")

    def __calcualte_grid_use(self,generation: float, consumption: float, battery_power: float):
        if battery_power < 0:
            battery_power * (-1)
        else:
            battery_power = 0
        
        if (generation - consumption - battery_power) > 0:
            return 0

        return (generation - consumption - battery_power)*(-1)
    
    def __calculate_pv_feed(self, generation: float, consumption: float, battery_power: float):
        if battery_power < 0:
            battery_power = 0
        
        if (generation - consumption - battery_power) < 0:
            return 0

        return (generation - consumption - battery_power)
    
    def __calculate_consumption_conver_by_pv(self, generation: float, consumption: float):
        if generation > consumption:
            return consumption
        else:
            return generation

    def print_simulated_data(self):
        print(self.simulation_result.df)
    