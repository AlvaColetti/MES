from matplotlib import markers
from Models.Consumer import Consumer
from Models.PVSystem import PV_System
from Models.EnergySystem import EnergySystem
from Models.analyzers.eco_analyzer import Eco_Analyzer
from Models.analyzers.financial_analyzer import Financial_Analyzer
from Models.battery_factory import Battery_factory
import matplotlib.pyplot as plt

PV_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV_Production.csv"
CONSUMER_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load_Production.csv"

factory = Battery_factory()


pv_powers = []
deckungs_grad = []

for i in range(1,8):

    LiB = factory.create_LiB_LFP_BYD_from_parameter("capacity", 40) #Building battery according to characteristic
    LiB.set_degradation_factors(1,1) #Degradation for power and capacity in %/a
    LiB.set_standby_losses(1) #losses per hour in %/h
    LiB.set_resolution_in_minutes(30) # setting system resolution

    pv = PV_System()
    pv.load_profile(PV_PROFILE_PATH)
    pv_power = 20 * i
    pv.size_pv_system(pv_power)

    consumer = Consumer()
    consumer.load_profile(CONSUMER_PROFILE_PATH)

    energySystem = EnergySystem(consumer,LiB,pv)
    energySystem.print_info()
    energySystem.simulate()

    eco_analyzer = Eco_Analyzer(energySystem.simulation_result)

    pv_powers.append(pv_power)
    deckungs_grad.append(round(eco_analyzer.contribution_margin * 100,2))


plt.plot(pv_powers, deckungs_grad, marker="o")
plt.xlim(0, 160)
plt.ylim(0,80)
plt.title("System Simulation with Lib Battery")
plt.ylabel("Solarer Deckungsgrad [%]")
plt.xlabel("PV Leistung [kW]")
plt.grid()
plt.show()

input("press a key to close the program\n")
