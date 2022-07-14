from models.battery import Battery

class BatteryFactory():

    def __init__(self) -> None:
        self.LIB_NMC_TESTVOLT_LOOKUP_TABLE = {"cost_for_capacity": 800} # Kosten der kWh, 800€ pro kWh für Li-NMC Akku
        self.LIB_LFP_BYD = {"cost_for_capacity": 800} # Kosten der kWh, 800€ pro kWh für Li-LFP Akku
        self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE = {"cost_for_capacity": 1000} # Kosten der kWh, 1000€ pro kWh für RFB Akku
        self.VRFB_VOLTERION_FRAUNHOFER_LOOKUP_TABLE = {"cost_for_capacity": 1000} # Kosten der kWh, 1000€ pro kWh für VRFB Akku

    def create_LiB_NMC_TestVolt_from_parameter(self,parameterName : str,  parameterValue : float):

        max_power = 76 # maximale Leistung gemäß Datenblatt
        min_power = 5 # minimale Leistung gemäß Datenblatt
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.LIB_NMC_TESTVOLT_LOOKUP_TABLE)

        output = Battery(capacity, min_power, max_power) # Erzeuge Objekt der Klasse "Battery" mit den zugewiesenen parameter
        output.technology = "LiB (Lithium NMC) (Testvolt)" # Bezeichnung für die Baterie festlegen
        output.set_efficiencies(98,98) # Effizienz der Batterie beim laden und entladen festlegen gemäß Datenblatt
        output.set_standby_losses(0)  # Verluste im Standby gemäß Datenblatt
        output.setCost(self.__calculate_cost_from_parameter(parameterName, parameterValue, self.LIB_NMC_TESTVOLT_LOOKUP_TABLE)) #Berechnet die Kosten entweder aus: zugewiesene Kosten oder Kapazität

        return output
    
    def create_LiB_LFP_BYD_from_parameter(self, parameterName: str, parameterValue: float):

        max_power = 60
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
        output.set_efficiencies(70,70) # wie hoch is hier die wirkungsgrad?? or this battery does not have one?
        output.set_standby_losses(1)
        output.setCost(self.__calculate_cost_from_parameter(parameterName, parameterValue, self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE))

        return output
    
    def create_VRFB_Volterion_Fraunhofer_from_parameter(self, parameterName: str, parameterValue: float):

        max_power = 15 # Default values can be change with the function modify_power()
        min_power = 5
        capacity = self.__calculate_capacity_from_parameter(parameterName, parameterValue, self.RFB_EISEN_SALZ_VOLTSTORAGE_LOOKUP_TABLE)

        output = Battery(capacity, min_power, max_power)
        output.technology = "VRFB (Volterion/Fraunhofer)"
        output.set_efficiencies(80,80) # wie hoch is hier die wirkungsgrad?? or this battery does not have one?
        output.set_standby_losses(1)
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