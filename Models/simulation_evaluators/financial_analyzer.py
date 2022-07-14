from models.battery import Battery
from models.dependecies.SimulationResult import SimulationResult

class FinancialEvaluator:
    def __init__(self, simulated_data: SimulationResult, battery:Battery) -> None:
        self.simulated_data =simulated_data
        self.feedIn_remuneration =  0
        self.total_feedIn_renumeration = 0
        self.energy_cost = 0
        self.savings_from_direct_pv_consumption = 0
        self.savings_from_battery = 0
        self.total_battery_operation_cost = 0
        self.battery = battery

    def set_feedIn_remuneration(self, value: float):
        self.feedIn_remuneration = value # euro per kWh
    
    def set_energy_cost(self, value:float):
        self.energy_cost = value # in euro per kWh
    
    def __calculate_savings_from_direct_pv_consumption(self):
        self.savings_from_direct_pv_consumption = self.simulated_data.df["Gedeckter Verbrauch aus PV [kW]"].sum() * self.simulated_data.resolution * self.energy_cost
    
    def __calculate_saving_from_battery(self):
        x = self.simulated_data.df[self.simulated_data.df["Ladungänderung [kWh]"] < 0].values.tolist()
        battery_outputs = self.simulated_data.df[self.simulated_data.df["Ladungänderung [kWh]"] < 0]
        self.savings_from_battery = (-1) * battery_outputs["Ladungänderung [kWh]"].sum() * self.energy_cost * self.battery.dechargingEffiency

    def __calculate_total_feedIn_remuneration(self):
        self.total_feedIn_renumeration = self.feedIn_remuneration * self.simulated_data.df["Einspeisung PV [kW]"].sum() * self.simulated_data.resolution

    def __calculate_battery_operation_cost(self):
        battery_output_energy_needed = self.simulated_data.df[self.simulated_data.df["Battery Leistungsdurchsatz [kW]"] < 0]
        grid_cost = self.energy_cost * battery_output_energy_needed["Battery Betrieb Energie [kWh]"].sum()

        battery_input_energy_needed = self.simulated_data.df[self.simulated_data.df["Battery Leistungsdurchsatz [kW]"] > 0]
        remuneration_cost = self.feedIn_remuneration * battery_input_energy_needed["Battery Betrieb Energie [kWh]"].sum()

        self.total_battery_operation_cost = grid_cost + remuneration_cost

    def calculate_savings(self):
        self.__calculate_saving_from_battery()
        self.__calculate_savings_from_direct_pv_consumption()
        self.__calculate_total_feedIn_remuneration()
        self.__calculate_battery_operation_cost()

    def print_info(self):
        message = "***Financial analysis*** \n"
        message += "\tEnergy cost: {} €/kWh || FeedIn Remuneration: {} €/kWh \n".format(self.energy_cost, self.feedIn_remuneration)
        message += "\tSavings from direct PV consumption: {} € \n".format(self.savings_from_direct_pv_consumption)
        message += "\tSavings from battery consumption: {} € \n".format(self.savings_from_battery)
        message += "\tBattery operation cost {} € \n".format(self.total_battery_operation_cost)
        message += "\tTotal feedIn remuneration: {} € \n".format(self.total_feedIn_renumeration)
        print(message)
    
    