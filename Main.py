from models.consumption import Consumption
from models.pv_system import PV_System
from models.energy_system import EnergySystem
from models.simulation_evaluators.sustainability_evaluator import SustainabilityEvaluator
from models.simulation_evaluators.financial_analyzer import FinancialEvaluator
from models.battery_factory import BatteryFactory

PV_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\PV_Production.csv"
CONSUMER_PROFILE_PATH = "C:\\Users\\alva-coletti\\Desktop\\MES\\Profiles\\Load_Production.csv"

factory = BatteryFactory() # erzeuge einen Objekt der Klasse Battery_factory

LiB = factory.create_LiB_LFP_BYD_from_parameter("capacity", 40) # erzeuge eine LFP Batterie mit einer Kapazität von 40kWh und lege ihre Parametern entsprechend den Datenblatt fest
LiB.set_degradation_factors(1,1) # setze die Degradation der Kapazität und der Leistung jeweils auf 1% pro Jahr
LiB.set_standby_losses(1) # setze die Standby-Verluste auf 1% pro Stunde
LiB.set_resolution_in_minutes(30) # Zeitliche Auflösung der Berechnungder Simulation auf 30 min

pv = PV_System() # erzeugt ein Objekt der Klasse PVSystem
pv.load_profile(PV_PROFILE_PATH)  # liest die PV-Daten aus der csv-datei ein.
pv.size_pv_system(100) # Skaliert die PV-Anlage nach Leistung in kW

consumer = Consumption() # erzeugt ein Objekt der Klasse Consumption
consumer.load_profile(CONSUMER_PROFILE_PATH) # liest der Lastprofil aus der csv-datei ein.

# Rf = factory.create_RFB_eisen_salz_VoltStorage_from_parameter("capacity", 40)
# Rf.set_degradation_factors(1,1)
# Rf.modify_power(15,5)
# Rf.set_operation_consumption(0.25*Rf.max_power)
# Rf.print_info()
# Rf.set_resolution_in_minutes(30)

energySystem = EnergySystem(consumer,LiB,pv) # erzeugt ein Energiesystem, von der Klasse EnergySystem, mit den eingelesenen Lastprofile, PV-Daten und die neue dimensionierte Batterie
energySystem.print_info() # Darstellt die Systemkenndaten
energySystem.simulate() # Ausführung der Simulation

eco_analyzer = SustainabilityEvaluator(energySystem.simulation_result)
eco_analyzer.print_info()

finance_analyzer = FinancialEvaluator(energySystem.simulation_result, LiB)
finance_analyzer.set_energy_cost(0.18) # Energiekosten in €/kWh
finance_analyzer.set_feedIn_remuneration(0.063) # Einspeisung Vergütung in €
finance_analyzer.calculate_savings() # Savings for one year in €
finance_analyzer.print_info()

margin = eco_analyzer.contribution_margin

input("press a key to close the program\n")
