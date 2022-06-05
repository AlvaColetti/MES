from Models.Battery import Battery

class Battery_factory():

    def __init__(self) -> None:
        self.BLEI_LOOKUP_TABLE = {"power_for_capacity":0.2, "cost_for_capacity": 300, "cost_for_power": 1500}
        self.LITHIUM_LOOKUP_TABLE = {"power_for_capacity":0.3, "cost_for_capacity": 300, "cost_for_power": 1500}
    

    def create_blei_battery_from_parameter(self,parameterName : str,  parameterValue : float):

        power = self.__calculate_power_from_parameter(parameterName, parameterValue, self.BLEI_LOOKUP_TABLE)
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.BLEI_LOOKUP_TABLE)

        output = Battery(power, capacity)
        output.technology = "Blei"
        output.set_efficiencies(95,95)
        output.set_standby_losses(1)

        return output
    
    def create_lithium_from_parameter(self, parameterName: str, parameterValue: float):
        power = self.__calculate_power_from_parameter(parameterName, parameterValue, self.LITHIUM_LOOKUP_TABLE)
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.LITHIUM_LOOKUP_TABLE)

        output = Battery(power, capacity)
        output.technology = "Lithium"
        output.set_efficiencies(98,98)
        output.set_standby_losses(1)

        return output
    
    def __calculate_power_from_parameter(self, parameterName: str, parameterValue: float, look_up_table):
        if (parameterName == "cost"):
            return parameterValue/look_up_table["cost_for_power"]
        if (parameterName == "power"):
            return parameterValue
        if (parameterName == "capacity"):
            return parameterValue * look_up_table["power_for_capacity"]
    
    def __calculate_capacity_from_parameter(self, parameterName: str, parameterValue: float, look_up_table):
        if (parameterName == "cost"):
            return parameterValue/look_up_table["cost_for_capacity"]
        if (parameterName == "capacity"):
            return parameterValue
        if (parameterName == "power"):
            return parameterValue / look_up_table["power_for_capacity"]