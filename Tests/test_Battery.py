import unittest
from Models.Battery import Battery

class test_Battery(unittest.TestCase):
    def setUp(self):
        self.sut = Battery(250,10,100)
        self.sut.set_resolution_in_minutes(15)
        self.sut.set_efficiencies(98, 98)

    def test_batterydefaultvalues(self):
        self.assertEqual(self.sut.capacity, 100)

    def test_calculate_power_throuhput(self):
        self.sut.calculate_power_throuhput(200)
        self.assertEqual(self.sut.power_throuhput, self.sut.max_power)

        self.sut.calculate_power_throuhput(self.sut.min_power -1)
        self.assertEqual(self.sut.power_throuhput, 0)

        self.sut.calculate_power_throuhput(self.sut.max_power - 1)
        self.assertEqual(self.sut.power_throuhput, self.sut.max_power -1)
    
    def test_calculate_demanded_energy_when_power_throuhput_smaller_than_minPower_should_be_cero(self):
        self.sut.calculate_power_throuhput(self.sut.min_power -1)
        demandedEnergy = self.sut.calculate_demanded_energy()
        self.assertEqual(demandedEnergy, 0)
    
    def test_calculate_demanded_energy_when_power_throuhput_higher_than_minPower(self):
        demanded_power = self.sut.min_power + 1
        self.sut.calculate_power_throuhput(self.sut.min_power +1)
        demandedEnergy = self.sut.calculate_demanded_energy()

        self.assertAlmostEqual(demandedEnergy, demanded_power*self.sut.Resolution, 0)
        self.assertGreater(demanded_power*self.sut.Resolution, demandedEnergy)
    
    def test_calculateStateEnergyChange_WhenOutputEnergyHigherThanCurrentState_ShouldBeCero(self):
        self.sut.state = 12
        self.sut.calculate_state_energy_change(-(self.sut.state + 1))
        self.assertEqual(self.sut.state, 0)

if __name__ == '__main__':
    unittest.main()