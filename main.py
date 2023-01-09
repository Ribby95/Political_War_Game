# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



class GameWorld():

    def __init__(self, numPlayers):
        self.num_players = numPlayers
        self.faction_list = ["Nobles", "Merchants", "Church", "King"]
        self.player_list = []
        self.territory_list = []

        self.turn_count = 0


    def getPlayers(self):
        #print(self.player_list)
        return self.player_list

    def getTerritories(self):
        return self.territory_list


    class Territory():
        def __init__(self, name):
            self.name = name

        def getTerritoryName(self):
            # print(self.player_list)
            return self.name



    #Inner class of GameWorld
    class Player():
        def __init__(self, name = "N/A", color = "", faction = ""):
            self.name = name
            self.color = color
            self.faction = faction
            self.assets = {
                "Territories": [],
                "Gold": 0,
                "Armies": []

            }

    #Inner class of GameWorld
    class Army():
        # want these to be global (maybe only to Army class) constants, but not sure about the best way to do it
        global UNIT_POWER_INFANTRY
        global UNIT_POWER_CAVALRY
        global UNIT_POWER_ARTILLERY

        UNIT_POWER_INFANTRY = 0.1
        UNIT_POWER_CAVALRY = 0.2
        UNIT_POWER_ARTILLERY = 0.3

        def __init__(self, powerValue = 0, color="", faction=""):

            self.power_value = powerValue
            self.composition = {
                'Infantry': 0,
                'Cavalry': 0,
                'Artillery': 0
            }

            self.color = color
            self.faction = faction

        def calculatePower(self):

            power =  UNIT_POWER_INFANTRY * self.composition['Infantry'] + UNIT_POWER_CAVALRY \
                     * self.composition['Cavalry'] + UNIT_POWER_ARTILLERY * self.composition["Artillery"]



        '''
        #Inner class of Army
        class Unit():
            def __init__(self, name="N/A", color="", faction=""):
                self.name = name
                self.color = color
                self.faction = faction
        '''


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    print("hello world")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
