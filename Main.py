from Models.Consumer import Consumer
from Models.PVSystem import PVSystem
from Models.Battery import Battery
from Models.EnergySystem import EnergySystem
from Models.battery_factory import Battery_factory

# PV_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV.csv"
# CONSUMER_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load.csv"

# pv = PVSystem()
# pv.load_profile(PV_PROFILE_PATH)

# consumer = Consumer()
# consumer.load_profile(CONSUMER_PROFILE_PATH)

# battery = Battery(15,5,0)
# battery.set_efficiencies(95,95)
# battery.set_operation_consumption(35)
# battery.set_resolution_in_minutes(15)

# energySystem = EnergySystem(consumer,battery,pv)
# energySystem.simulate()

# battery.print_info()
# print(energySystem.dfSimulationResult)

factory = Battery_factory()
bleiBattery = factory.create_blei_battery_from_parameter("power", 20)
lithiumBattery = factory.create_lithium_from_parameter("power", 20)

bleiBattery.print_info()
lithiumBattery.print_info()

input("press a key to close the program")