from turtle import pencolor
from Models.Consumer import Consumer
from Models.PVSystem import PVSystem
from Models.Battery import Battery
from Models.EnergySystem import EnergySystem

print("===========================\n    Welcome MES\n===========================")
profile = Consumer()
profile.LoadProfile("C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load.csv")
pv = PVSystem()
pv.LoadProfile("C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV.csv")
battery = Battery(15,5,0)
battery.set_efficiencies(95,95)
battery.set_resolution_in_minutes(30)

energySystem = EnergySystem(profile,battery,pv)
energySystem.simulate()
input("press a key to close the program")