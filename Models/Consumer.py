from tokenize import Double
from typing_extensions import Self

import pandas as pd

from Models.dependecies.csvLoader import CsvLoader

class Consumer(CsvLoader):
    def __init__(self) -> None:
        pass

    def GetPeak(self) -> float:
         max(self.profile)
    
    def GetBaseLoad(self) -> float:
        min(self.profile)
