from Models.Consumer import Consumer
from Models.PVSystem import PV_System
from Models.EnergySystem import EnergySystem
from Models.analyzers.eco_analyzer import Eco_Analyzer
from Models.analyzers.financial_analyzer import Financial_Analyzer
from Models.battery_factory import Battery_factory

PV_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV_Production.csv"
CONSUMER_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load_Production.csv"

factory = Battery_factory()

LiB = factory.create_LiB_LFP_BYD_from_parameter("capacity", 40) #Building battery according to characteristic
LiB.set_degradation_factors(1,1) #Degradation for power and capacity in %/a
LiB.set_standby_losses(1) #losses per hour in %/h
LiB.set_resolution_in_minutes(30) # setting system resolution
LiB.print_info() # displaying battery information

pv = PV_System()
pv.load_profile(PV_PROFILE_PATH)
pv.size_pv_system(40) # Pv system seize in kW

consumer = Consumer()
consumer.load_profile(CONSUMER_PROFILE_PATH)

# Rf = factory.create_RFB_eisen_salz_VoltStorage_from_parameter("capacity", 40)
# Rf.set_degradation_factors(1,1)
# Rf.modify_power(15,5)
# Rf.set_operation_consumption(0.25*Rf.max_power)
# Rf.print_info()
# Rf.set_resolution_in_minutes(15)


energySystem = EnergySystem(consumer,LiB,pv)
energySystem.simulate()
energySystem.save_as_excel(energySystem.battery.technology)

eco_analyzer = Eco_Analyzer(energySystem.simulation_result)
eco_analyzer.print_info()

finance_analyzer = Financial_Analyzer(energySystem.simulation_result)
finance_analyzer.set_energy_cost(0.3) # Energiekosten in €
finance_analyzer.set_feedIn_remuneration(0.065) # Einspeisung Vergütung in €
finance_analyzer.calculate_savings() # Savings for one year in €
finance_analyzer.print_info()

margin = eco_analyzer.contribution_margin

input("press a key to close the program\n")
