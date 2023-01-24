from game_world import Faction, Territory
from lobby import Lobby

def main():
    nobles=Faction("Nobles", color="red")
    merchants = Faction("Merchants", color="Brown")
    church = Faction("Church", color="Blue")
    king = Faction("King", color="purple")

    territories = [
        Territory("Richmond City", merchants),
        Territory("Washington DC", king)
    ] + [Territory(x, nobles) for x in ("Fairfax", "Loudoun")]


    lobby = Lobby(
        players=[],
        territories=territories,
        landless_factions= [church]
    )
    lobby.setup_menu()
    lobby.wait_for_players()
    world1 = lobby.start_game()

if __name__ == '__main__':
    main()


