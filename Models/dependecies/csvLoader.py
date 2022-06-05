import pandas as pd
import string
from tkinter.tix import MAX
from tokenize import Double
from typing_extensions import Self

class CsvLoader:
    def __init__(self) -> None:
        self.profile : pd.DataFrame
        pass

    def load_profile(self, profileCsv : string ):
        self.profile = pd.read_csv(profileCsv, delimiter=";")
    
    def get_profile_count(self):
        return len(self.profile)