import pandas as pd
from Models.Consumer import Consumer
from Models.Battery import Battery
from Models.PVSystem import PV_System
from Models.dependecies.SimulationResult import SimulationResult

class EnergySystem:
    
    def __init__(self, consumer: Consumer, battery: Battery, pvSystem: PV_System):
        self.consumer = consumer
        self.pvSystem = pvSystem
        self.battery = battery
        self.checkDataFrames()

        self.simulation_result = SimulationResult(self.battery)
    
    def simulate(self):
        max_counts = self.consumer.get_profile_count()-1
        for i in range(0,max_counts):

            uhrzeit = self.consumer.profile.loc[i,"Uhrzeit"]
            consumption = self.consumer.profile.loc[i,"Leistung"]
            generation = self.pvSystem.profile.loc[i,"Leistung"]
            demandedPower = float(generation)-float(consumption)
            
            self.battery.simulate_responde(demandedPower)
            battery_power = self.battery.power_throuhput
            battery_energy_change = self.battery.stateChange
            
            new_row = pd.DataFrame({'Uhrzeit': uhrzeit, 'PV Erzeugung [kW]': generation, 'Verbrauch [kW]': consumption,
            'Netz Nutzung [kW]' : round(self.__calcualte_grid_use(generation, consumption, battery_energy_change),2),
            'Gedeckter Verbrauch aus PV [kW]' : round(self.__calculate_consumption_conver_by_pv(generation, consumption)),
            'Einspeisung PV [kW]': self.__calculate_pv_feed(generation, consumption, battery_energy_change),
            'Battery Leistungsdurchsatz [kW]': round(demandedPower, 2), 'Battery Ladezustand [kWh]': round(self.battery.state,5),
            'Ladungänderung [kWh]' : round(battery_energy_change,2) ,
            'Battery Betrieb Verbrauch [kW]' : self.battery.current_operation_consumption,
            'Battery Betrieb Energie [kWh]' :self.battery.operation_energy},
            index = [0])

            self.simulation_result.add_new_row(new_row)

            self.__show_simulation_progess(i,max_counts)
    
        self.simulation_result.df = self.simulation_result.df.sort_index(ascending=False)

    def __show_simulation_progess(self, current:int, last:int):
        progress = current/last * 100
        if (progress != 100):
            print("Loading: " + str(round(progress,1)) + "%" , end="\r")
        else:
            print("Simulation completed")

    def checkDataFrames(self):
        if self.consumer.get_profile_count() != self.pvSystem.get_profile_count():
            raise Exception("The data frames do not have the same length")

    def __calcualte_grid_use(self,generation: float, consumption: float, battery_energy: float):
        battery_power = battery_energy / self.battery.Resolution
        if battery_power < 0:
            battery_power * (-1)
        else:
            battery_power = 0
        
        if (generation - consumption - battery_power) > 0:
            return 0

        return (generation - consumption - battery_power)*(-1)
    
    def __calculate_pv_feed(self, generation: float, consumption: float, battery_energy: float):
        battery_power = battery_energy / self.battery.Resolution
        if battery_power < 0:
            battery_power = 0
        
        if (generation - consumption - battery_power) < 0:
            return 0

        return round((generation - consumption - battery_power),2)
    
    def __calculate_consumption_conver_by_pv(self, generation: float, consumption: float):
        if generation > consumption:
            return consumption
        else:
            return generation
    
    def save_as_excel(self,file:str):
        self.simulation_result.df.to_excel("{}.xlsx".format(file))

    def print_simulated_data(self):
        print(self.simulation_result.df)

    def print_info(self):
        self.pvSystem.print_info()
        self.battery.print_info()
        self.consumer.print_info()
        
    