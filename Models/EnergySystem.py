from Models.Consumer import Consumer
from Models.Battery import Battery
from Models.PVSystem import PVSystem


class EnergySystem:
    
    def __init__(self, consumer: Consumer, battery: Battery, pvSystem: PVSystem):
        self.loadProfile = consumer
        self.battery = battery
        self.pvSystem = pvSystem
        self.checkDataFrames()
    
    def simulate(self):
        for i in range(0,len(self.loadProfile.profile)-1):
            consumption = self.loadProfile.profile.iloc[i,0]
            generation = self.pvSystem.profile.iloc[i,0]
            self.battery.simulate_responde(float(generation)-float(consumption))
            
            print("/{}/".format(i))
            print("Consumption: {} kW / Generation: {} kW".format(consumption,generation))
            self.battery.print_info(i)
            print("\n")

    def checkDataFrames(self):
        if len(self.loadProfile.profile) != len(self.pvSystem.profile):
            raise Exception("The data frames do not have the same length")