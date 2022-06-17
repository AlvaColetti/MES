from Models.Consumer import Consumer
from Models.PVSystem import PVSystem
from Models.EnergySystem import EnergySystem
from Models.analyzers.eco_analyzer import Eco_Analyzer
from Models.analyzers.financial_analyzer import Financial_Analyzer
from Models.battery_factory import Battery_factory

PV_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV.csv"
CONSUMER_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load.csv"

pv = PVSystem()
pv.load_profile(PV_PROFILE_PATH)

consumer = Consumer()
consumer.load_profile(CONSUMER_PROFILE_PATH)

# creating Battery
factory = Battery_factory()

LiB = factory.create_LiB_LFP_BYD_from_parameter("capacity", 40)
LiB.set_degradation_factors(1,1)
LiB.set_standby_losses(1)
LiB.print_info()
LiB.set_resolution_in_minutes(15)

Rf = factory.create_RFB_eisen_salz_VoltStorage_from_parameter("capacity", 40)
Rf.set_degradation_factors(1,1)
Rf.modify_power(15,5)
Rf.set_operation_consumption(0.25*Rf.max_power)
Rf.print_info()
Rf.set_resolution_in_minutes(15)


energySystem = EnergySystem(consumer,Rf,pv)
energySystem.simulate()
energySystem.simulation_result.df.to_excel("{}.xlsx".format(energySystem.battery.technology)) # in case you want to analyse the simulated data in detail

eco_analyzer = Eco_Analyzer(energySystem.simulation_result)
eco_analyzer.print_info()

finance_analyzer = Financial_Analyzer(energySystem.simulation_result)
finance_analyzer.set_energy_cost(0.3)
finance_analyzer.set_feedIn_remuneration(0.065)
finance_analyzer.calculate_savings()
finance_analyzer.print_info()

margin = eco_analyzer.contribution_margin

input("press a key to close the program")
