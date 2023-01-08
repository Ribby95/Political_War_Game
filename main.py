# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class GameWorld():
    def __init__(self, numPlayers):
        self.num_players = numPlayers
        self.faction_list = ["Nobles", "Merchants", "Church", "King"]
        self.player_list = []

        self.turn_count = 0


    def getPlayers(self):
        print(self.player_list)
        return self.player_list


class Player():
    def __init__(self, name = "N/A", color = "", faction = ""):
        self.name = name
        self.color = color
        self.faction = faction



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("hello world")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
