
class Army:
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

    def calculatePower(self):
        power = Army.UNIT_POWER_INFANTRY * self.composition['Infantry'] + \
                Army.UNIT_POWER_CAVALRY  * self.composition['Cavalry'] + \
                Army.UNIT_POWER_ARTILLERY * self.composition["Artillery"]
        return power
    '''
    #Inner class of Army
    class Unit():
        def __init__(self, name="N/A", color="", faction=""):
            self.name = name
            self.color = color
            self.faction = faction
    '''