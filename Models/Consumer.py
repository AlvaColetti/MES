from tokenize import Double
from typing_extensions import Self

import pandas as pd

from Models.dependecies.csvLoader import CsvLoader

class Consumer(CsvLoader):
    def __init__(self) -> None:
        pass

    def GetPeak(self) -> float:
        return self.profile["Leistung"].max()
    
    def GetBaseLoad(self) -> float:
        return self.profile["Leistung"].min()
    
    def print_info(self):
        message = "***Consumer***\n"
        message += "\t Peak load: " + str(self.GetPeak()) + " kW\n"
        message += "\t Base load: " + str(self.GetBaseLoad()) + " kW\n\n"
        print(message)
