
class Army():
    # want these to be global constants (maybe only to Army class), but not sure about the best way to do it
    global UNIT_POWER_INFANTRY
    global UNIT_POWER_CAVALRY
    global UNIT_POWER_ARTILLERY

    UNIT_POWER_INFANTRY = 0.1
    UNIT_POWER_CAVALRY = 0.2
    UNIT_POWER_ARTILLERY = 0.3

    def __init__(self, powerValue=0, color="", faction=""):

        self.composition = {
            'Infantry': 0,
            'Cavalry': 0,
            'Artillery': 0
        }

        self.color = color
        self.faction = faction
        self.power_value = self.calculatePower()

    def calculatePower(self):
        power = UNIT_POWER_INFANTRY * self.composition['Infantry'] + UNIT_POWER_CAVALRY \
                * self.composition['Cavalry'] + UNIT_POWER_ARTILLERY * self.composition["Artillery"]
        return power
    '''
    #Inner class of Army
    class Unit():
        def __init__(self, name="N/A", color="", faction=""):
            self.name = name
            self.color = color
            self.faction = faction
    '''