import pandas as pd
from models.consumption import Consumption
from models.battery import Battery
from models.pv_system import PV_System
from models.dependecies.SimulationResult import SimulationResult

class EnergySystem:
    
    def __init__(self, consumption: Consumption, battery: Battery, pv_system: PV_System):
        self.consumer = consumption
        self.pvSystem = pv_system
        self.battery = battery
        self.checkDataFrames() # Überprüft dass die Dataframe (Profiles) der Consumption und PV-Anlage genau groß sind

        self.simulation_result = SimulationResult(self.battery)
    
    def simulate(self):
        max_counts = self.consumer.get_profile_count()-1
        for i in range(0,max_counts):

            current_time = self.consumer.profile.loc[i,"Uhrzeit"] # liest die Zeit Zeilenweise
            consumption = self.consumer.profile.loc[i,"Leistung"] # liest die Lasthoche
            generation = self.pvSystem.profile.loc[i,"Leistung"] # liest die generierte Leistung vom PV-System Zeilenweise
            power_difference = generation-consumption # berechnet die Liestungsunterschied
            
            self.battery.simulate_responde(power_difference)
            
            new_row = pd.DataFrame({'Uhrzeit': current_time, 'PV Erzeugung [kW]': generation, 'Verbrauch [kW]': consumption,
            'Netz Nutzung [kW]' : self.__calcualte_grid_use(generation, consumption, self.battery.charge_change),
            'Gedeckter Verbrauch aus PV [kW]' : self.__calculate_consumption_conver_by_pv(generation, consumption),
            'Einspeisung PV [kW]': self.__calculate_pv_feed(generation, consumption, self.battery.charge_change),
            'Verbrauch-Erzeugung Leistungsunterschied [kW]': power_difference, 
            'Battery Ladezustand [kWh]': self.battery.state_of_charge,
            'Ladungsänderung [kWh]' : self.battery.charge_change,
            'Batterie Betrieb Verbrauch [kW]' : self.battery.current_operation_consumption,
            'Batterie Betrieb Energie [kWh]' :self.battery.operation_energy},
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
        
    