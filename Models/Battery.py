import numpy

class Battery:

    def __init__(self, capacity: float, maxPower: float, initialState: float = 0 ):
        """ 
        Retunrs
        --------
            Battery Model

        Parameters
        ----------
            capacity: float
                the maximum battery capacity in kWh
            
            maxpower: float
                the maximum battery output and input power in kW
            
            initalState: float
                kWh of saved energy at the start of the simulation
    
        """
        self.capacity = capacity
        self.maxPower = maxPower
        self.state = initialState
        self.chargingEffiency = 1
        self.dechargingEffiency = 1
        self.standByLosses = 0
        self.Resolution = 1

        self.powerThrouhput = 0

    
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
    
    def set_standby_losses(self, hourly_loss: float):
        """
            Sets
            ----
                The battery standby losses per hour
            
            Parameters
            ----------
            hourly_loss: float
                losses per hour pass relative to the current state in %
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

    def __calculate_state_energy_change(self, demandedEnergy):      
        """
            Calculates the new battery state
            
            Parameters
            ----------
            minutes: float
                new resolution in minutes
        """
        self.state = self.state*self.__calculate_standby_efficiency()

        if self.state + demandedEnergy >= self.capacity:
            self.state = self.capacity
        elif self.state + demandedEnergy < 0:
            self.state = 0
        else:
            self.state = self.state + demandedEnergy
    
    def __calculate_power_throughput(self, demandedPower):
        if self.maxPower <= abs(demandedPower):
            self.powerThrouhput = self.maxPower*numpy.sign(demandedPower)
        elif self.maxPower > abs(demandedPower):
            self.powerThrouhput = demandedPower
    
    def __calculate_demanded_energy(self):
        if numpy.sign(self.powerThrouhput) == 1:
            return self.powerThrouhput*self.chargingEffiency*self.Resolution
        else:
            return self.powerThrouhput/ self.dechargingEffiency * self.Resolution
    
    def simulate_responde(self, demandedPower):
        self.__calculate_power_throughput(demandedPower)
        demanded_energy = self.__calculate_demanded_energy()
        self.__calculate_state_energy_change(demanded_energy)

    def print_info(self, index):
        print("{} // Current energy storaged {} kWh \n last power throuput {} kW".format(index, self.state, self.powerThrouhput))
