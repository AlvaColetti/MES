from models.consumption import Consumption
from models.pv_system import PV_System
from models.energy_system import EnergySystem
from models.simulation_evaluators.sustainability_evaluator import SustainabilityEvaluator
from models.simulation_evaluators.financial_analyzer import FinancialEvaluator
from models.battery_factory import BatteryFactory
import matplotlib.pyplot as plt

PV_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV_Production.csv"
CONSUMER_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load_Production.csv"

factory = BatteryFactory()

capacities = [76,100]

for cap in capacities:
    x_achse = []
    deckungs_grad = []
    for i in range(1,8):
        LiB = factory.create_LiB_NMC_TestVolt_from_parameter("capacity", cap) #Building battery according to characteristic
        LiB.set_degradation_factors(1,1) #Degradation for power and capacity in %/a
        LiB.set_standby_losses(0) #losses per hour in %/h
        LiB.set_resolution_in_minutes(30) # setting system resolution
        LiB.max_power = 2.5 * (i-1)

        pv = PV_System()
        pv.load_profile(PV_PROFILE_PATH)
        pv_power = 150
        pv.size_pv_system(pv_power)

        consumer = Consumption()
        consumer.load_profile(CONSUMER_PROFILE_PATH)

        energySystem = EnergySystem(consumer,LiB,pv)
        energySystem.print_info()
        energySystem.simulate()

        eco_analyzer = SustainabilityEvaluator(energySystem.simulation_result)

        x_achse.append(LiB.max_power)
        deckungs_grad.append(round(eco_analyzer.contribution_margin * 100 , 2))

    plt.plot(x_achse, deckungs_grad, marker="o", label= LiB.technology + " mit " + str(cap) + " kWh Kapazität")
    print(deckungs_grad)


plt.xlim(5, 17.5)
plt.ylim(40,80)
plt.title("Systemsimulation mit" + LiB.technology + " und " + str(pv.installed_power) + " % Solarfeld")
plt.ylabel("Solarer Deckungsgrad [%]")
plt.xlabel("Leistung der Batterie [kW]")
plt.legend()
plt.grid()
plt.show()

input("press a key to close the program\n")
