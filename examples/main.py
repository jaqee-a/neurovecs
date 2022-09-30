from game import Game
from multidrone import GameMultiDrone
from simulation.imguiapp import ImGuiApp

imGuiApp : ImGuiApp()

if __name__ == "__main__":
    #GameMultiDrone()
    Game()
    print("fff")
    print(imGuiApp.selectedCamouflageMode)
    if imGuiApp.selectedCamouflageMode == 4 :
        print("fff")