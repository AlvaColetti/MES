from Models.Consumer import Consumer
from Models.Battery import Battery
from Models.PVSystem import PVSystem


class EnergySystem:
    
    def __init__(self, consumer: Consumer, battery: Battery, pvSystem: PVSystem):
        self.loadProfile = consumer
        self.pvSystem = pvSystem
        self.battery = battery
        self.checkDataFrames()
    
    def simulate(self):
        for i in range(0,len(self.loadProfile.profile)-1):
            consumption = self.loadProfile.profile.iloc[i,0]
            generation = self.pvSystem.profile.iloc[i,0]
            
            demandedEnergy = float(generation)-float(consumption)
            self.battery.simulate_responde(demandedEnergy)
            
            print("/{}/".format(i))
            print("Consumption: {} kW / Generation: {} kW".format(consumption,generation))
            self.battery.print_info(i)
            print("\n")

    def checkDataFrames(self):
        if len(self.loadProfile.profile) != len(self.pvSystem.profile):
            raise Exception("The data frames do not have the same length")