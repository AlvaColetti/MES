from Models.Battery import Battery

class Battery_factory():

    def __init__(self) -> None:
        self.LIB_NMC_TESTVOLT_LOOKUP_TABLE = {"cost_for_capacity": 800}
        self.LIB_LFP_BYD = {"cost_for_capacity": 800}
        self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE = {"cost_for_capacity": 1000}
        self.VRFB_VOLTERION_FRAUNHOFER_LOOKUP_TABLE = {"cost_for_capacity": 1000}

    def create_LiB_NMC_TestVolt_from_parameter(self,parameterName : str,  parameterValue : float):

        max_power = 76 # Default values can be change with the function modify_power()
        min_power = 5
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.LITHIUM_NMC_TESTVOLT_LOOKUP_TABLE)

        output = Battery(min_power, max_power, capacity)
        output.technology = "LiB (Lithium NMC) (Testvolt)"
        output.set_efficiencies(98,98)
        output.set_standby_losses(0)
        output.setCost(self.__calculate_cost_from_parameter(parameterName, parameterValue, self.LITHIUM_NMC_TESTVOLT_LOOKUP_TABLE))

        return output
    
    def create_LiB_LFP_BYD_from_parameter(self, parameterName: str, parameterValue: float):

        max_power = 75 # Default values can be change with the function modify_power()
        min_power = 5
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.LIB_LFP_BYD)

        output = Battery(capacity, min_power, max_power, )
        output.technology = "LiB (LFP) (BYD)"
        output.set_efficiencies(95,95)
        output.set_standby_losses(0)
        output.setCost(self.__calculate_cost_from_parameter(parameterName, parameterValue, self.LIB_LFP_BYD))

        return output

    def create_RFB_eisen_salz_VoltStorage_from_parameter(self, parameterName: str, parameterValue: float):

        max_power = 10 # Default values can be change with the function modify_power()
        min_power = 5
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE)

        output = Battery(capacity, min_power, max_power)
        output.technology = "RFB -Eisen-Salz( Voltstorage) "
        output.set_efficiencies(95,95) # wie hoch is hier die wirkungsgrad?? or this battery does not have one?
        output.set_standby_losses(0)
        output.setCost(self.__calculate_cost_from_parameter(parameterName, parameterValue, self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE))

        return output
    
    def create_VRFB_Volterion_Fraunhofer_from_parameter(self, parameterName: str, parameterValue: float):

        max_power = 15 # Default values can be change with the function modify_power()
        min_power = 5
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE)

        output = Battery(capacity, min_power, max_power)
        output.technology = "VRFB (Volterion/Fraunhofer)"
        output.set_efficiencies(95,95) # wie hoch is hier die wirkungsgrad?? or this battery does not have one?
        output.set_standby_losses(0)
        output.setCost(self.__calculate_cost_from_parameter(parameterName, parameterValue, self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE))

        return output
    
    def __calculate_capacity_from_parameter(self, parameterName: str, parameterValue: float, look_up_table):
        if (parameterName == "cost"):
            return parameterValue/look_up_table["cost_for_capacity"]
        if (parameterName == "capacity"):
            return parameterValue
        if (parameterName == "power"):
            return parameterValue / look_up_table["power_for_capacity"]
    
    def __calculate_cost_from_parameter(self, parameterName: str, parameterValue: float, look_up_table):
        if (parameterName == "capacity"):
            return look_up_table["cost_for_capacity"]*parameterValue
        if (parameterName == "cost"):
            return parameterValue
    
    
    
    # def __calculate_power_from_parameter(self, parameterName: str, parameterValue: float, look_up_table):
    #     if (parameterName == "cost"):
    #         return parameterValue/look_up_table["cost_for_power"]
    #     if (parameterName == "power"):
    #         return parameterValue
    #     if (parameterName == "capacity"):
    #         return parameterValue * look_up_table["power_for_capacity"]