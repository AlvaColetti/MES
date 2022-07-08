from Models.dependecies.csvLoader import CsvLoader


class PV_System(CsvLoader):
    
    def __init__(self):
        self.installed_power = 0
        pass

    def size_pv_system(self,pv_leistung: float):
        """ 
        Sets the 
        ----------
            size of the PV System in kW
        """
        self.installed_power = pv_leistung
        self.profile['Leistung'] = self.profile['Leistung'].apply(lambda x: x*pv_leistung)
    
    def print_info(self):
        message = "***PV System***\n"
        message += "\t Peak generated Leistung: " + str(self.profile["Leistung"].max()) + " kW\n"
        message += "\t installierte Lesitung: " + str(self.installed_power) + " kWp\n\n"
        print(message)