from Models.dependecies.SimulationResult import SimulationResult

class Eco_Analyzer:
    def __init__(self, simulated_data: SimulationResult) -> None:
        self.simulated_data =simulated_data
        self.contribution_margin = self.__calculate_contribution_margin()
    
    def __calculate_contribution_margin(self):
        grid_use = self.simulated_data.df["Netz Nutzung [kW]"].sum()
        consumption = self.simulated_data.df["Verbrauch [kW]"].sum()
        return (consumption - grid_use) / consumption
    
    def print_info(self):
        message = "***Eco analysis***\n"
        message += "\tcontribution margin: {} % \n".format(round(self.contribution_margin * 100,2))
        print(message)