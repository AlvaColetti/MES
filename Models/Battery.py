import numpy

class Battery:

    def __init__(self, capacity: float, minPower:float, maxPower: float, initial_state_of_charge: float = 0 ):
        """ 
        Retunrs
        --------
            Battery Model

        Parameters
        ----------
            capacity: float
                the maximum battery capacity in kWh
            
            max_power: float
                the maximum battery output and input power in kW
            
            min_power: float
                the minimum battery output and input power in kW
            
            initalState: float
                kWh of saved energy at the start of the simulation
    
        """
        # capacity
        self.capacity = capacity # maximale Kapazität in kWh
        self.state_of_charge = initial_state_of_charge # Aktuele Ladungszustand in kWh
        self.charge_change = 0 # Ladungsänderung in kWh

        # power
        self.max_power = maxPower # Maximale Leistung in kW
        self.min_power = minPower # Minimale Leistung in kW
        self.regulated_power = 0 # Leistung zu/aus der Batterie in kW

        # efficiencies
        self.chargingEffiency = 1 # Verluste bei Ladung in %
        self.dechargingEffiency = 1 # Verluste bei Entladung in %
        self.standByLosses = 0 # Verluste bei Standby in %

        # operation consumption
        self.operation_consumption = 0 
        self.current_operation_consumption = 0
        self.operation_energy = 0

        # simulation parameters
        self.Resolution = 1 # zeitliche Auflösung der Simulation
        self.technology = "Undefined" # Art der Technologie 

        #Cost
        self.installation_cost = 0 # Installationskosten in Euro

        #Degradation factors
        self.capacity_degradation = 0 # Degradation in % per year
        self.power_degradation = 0 # Degradation % per year of maximum power
    
    def set_operation_consumption(self, operation_consumption: float):
        """ 
        Sets
        --------
            Operation consumption of the battery. Energy needed so that the battery can work

        Parameters
        ----------
            operation_consumption: float
                consumption in W
        """
        self.operation_consumption = operation_consumption

    def set_efficiencies(self, chargingEffiency: float, dechargingEfficiency: float):
        """ 
        Sets
        --------
            The battery effiencies for the simulator per default the efficiencies are set to 100%

        Parameters
        ----------
            chargingEffiency: float
                effiency at charging the battery in %
            
            dechargingEfficiency: float
                effiency at decharging the battery in %

        """
        self.chargingEffiency = chargingEffiency/100
        self.dechargingEffiency = dechargingEfficiency/100
    
    def simulate_responde(self, power_difference):
        self.state_of_charge = self.state_of_charge*self.__calculate_standby_efficiency() # Aktuellen Ladezustand nach Standby-Verlust einstellen
        self.calculate_regulated_power(power_difference) # Berechnung der eingestellte Leistung der Batterie
        needed_capacity = self.calculate_needed_capacity() # Berechnung der notwendige Kapazität im ideal Fall
        self.calculate_state_charge_change(needed_capacity) # Berechnung der Änderung der Ladezustand
        self.degradate() # Ausführung der degradation
    
    def set_standby_losses(self, hourly_loss: float):
        """
            Sets
            ----
                The battery standby losses per hour
            
            Parameters
            ----------
            hourly_loss: float
                losses per hour relative to the current state in %
        """
        if (hourly_loss > 1):
            raise ValueError('Losses per hour are to high')
        self.standByLosses = hourly_loss

    def set_resolution_in_minutes(self,minutes:int):
        """
            Set
            ---
                The hourly resoultion for the calculations
            
            Parameters
            ----------
            minutes: float
                new resolution in minutes
        """
        self.Resolution = minutes/60

    def __calculate_standby_efficiency(self):
        return (1-(self.standByLosses/100)*self.Resolution)

    def calculate_state_charge_change(self, demandedEnergy):
        previousState = self.state_of_charge

        if self.state_of_charge + demandedEnergy >= self.capacity:
            self.state_of_charge = self.capacity
        elif self.state_of_charge + demandedEnergy < 0:
            self.state_of_charge = 0
        else:
            self.state_of_charge = self.state_of_charge + demandedEnergy
        
        self.charge_change = self.state_of_charge - previousState

        self.__check_energy_consumption_ratio(previousState)
    
    def calculate_regulated_power(self, demandedPower: float):
        
        if self.min_power > abs(demandedPower):
            self.regulated_power = 0
            self.current_operation_consumption = 0

        elif self.max_power <= abs(demandedPower):
            self.regulated_power = self.max_power*numpy.sign(demandedPower)
            self.current_operation_consumption = self.operation_consumption

        elif self.max_power > abs(demandedPower) and self.min_power <= abs(demandedPower):
            self.regulated_power = demandedPower
            self.current_operation_consumption = self.operation_consumption
    
    def calculate_needed_capacity(self):
        if numpy.sign(self.regulated_power) == 1:
            return (self.regulated_power * self.chargingEffiency) * self.Resolution
        else:
            return (self.regulated_power / self.dechargingEffiency) * self.Resolution
    
    def __check_energy_consumption_ratio(self, previousState: float):
        self.operation_energy = self.current_operation_consumption * self.Resolution
        
        if (abs(self.charge_change) < self.current_operation_consumption*self.Resolution):
            self.operation_energy = 0
            self.charge_change = 0
            self.state_of_charge = previousState
            self.current_operation_consumption = 0

    def setCost(self, installationCost: float):
        self.installation_cost = installationCost
    
    def modify_power(self, max_power:float, min_power: float):
        self.max_power = max_power
        self.min_power = min_power

    def set_degradation_factors(self, capacity_degradation, power_degradation: float):
        self.capacity_degradation = capacity_degradation
        self.power_degradation = power_degradation

    def degradate(self):
        minutes_per_year = 365 * 24 * 60
        self.max_power = round( self.max_power * ( 1 - (self.power_degradation / 100 /  minutes_per_year) * self.Resolution), 2)
        self.capacity = round( self.capacity * ( 1 - (self.capacity_degradation / 100 /  minutes_per_year) * self.Resolution), 2)

    def print_info(self):
        info = "***Battery specifications***\n" + "\tcapacity [kWh]: {} || maximum power [kW]: {} || min power [kW]: {}\n"
        info += "\tcharging efficiency [%]: {} || decharging efficiency [%]: {} || standby losses [%/h]: {} \n"
        info += "\tcapacity degradation [%/a]: {} || power degradation [%/a]: {} \n"
        info += "\tInstallation cost [€]: {}\n"
        info = info.format(self.capacity, self.max_power, self.min_power, self.chargingEffiency *100, self.dechargingEffiency * 100, self.standByLosses,
        self.capacity_degradation, self.power_degradation, self.installation_cost)

        print(info)