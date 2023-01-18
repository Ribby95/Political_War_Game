import random
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



class GameWorld():

    def __init__(self):
        self.num_players = 0
        self.faction_list = ["Nobles", "Merchants", "Church", "King"]
        self.player_list = []
        self.territory_list = []

        self.faction_starting_territories = {
            "Nobles": ["Fairfax", "Loudoun"],
            "Merchants": ["Richmond City"],
            "Church": [],
            "King": ["Washington DC"]

        }

        self.turn_count = 0
        self.show_menu()
        self.make_lobby()


    def getPlayers(self):
        #print(self.player_list)
        return self.player_list

    def getTerritories(self):
        return self.territory_list

    def setPlayers(self,num):
        if type(num) == int and 1 <= num <= 4:
            self.num_players = num
        else:
           # print("Invalid number of players")
            return False

    def show_menu(self):
        players = ""
        while self.setPlayers(players) == False:
            players = int(input("Enter number of players (1-4): "))
            self.setPlayers(players)


    class Territory():
        def __init__(self, name):
            self.name = name

        def getTerritoryName(self):
            # print(self.player_list)
            return self.name

    class Player():
        def __init__(self, name="N/A", color="", faction=""):
            self.name = name
            self.color = color
            self.faction = faction
            self.assets = {
                "Territories": [],
                "Gold": 1000,
                "Armies": []

            }

    def make_lobby(self):
        prep = True
        while prep:

            for i in range(1, self.num_players + 1):
                player = input(f"Enter player {i} name: ")
                self.player_list.append(player)

            faction_temp = self.faction_list
            for player in self.player_list:
                faction = random.choice(faction_temp)
                print(f"{player} is: {faction}")
                faction_temp.remove(faction)

                new_player = self.Player(name=player, faction=faction)
                new_player.assets["Territories"] = self.faction_starting_territories[faction]
                self.player_list.append(new_player)
            prep = False

    def combat_simulator(self, army_list):
        pass

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    world1 = GameWorld()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
