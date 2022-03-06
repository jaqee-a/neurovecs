from typing import List

import numpy as np
import imgui

class ImGuiApp:

    selectedMovementMode: int = 0
    selectedCamouflageMode: int = 0

    speed : List[float] = []
    errors: List[float] = []
    RESOLUTION: int     = 4

    prey_trajectory: bool = True
    pred_trajectory: bool = True

    def __init__(self) -> None:
        pass

    def startSimulationFunc(self):
        pass

    def takeScreenshotFunction(self):
        pass

    def render(self):
        imgui.begin("Control Panel", True)
        #if imgui.tree_node("Trajectoire", imgui.TREE_NODE_DEFAULT_OPEN):
        #    _, self.prey_trajectory = imgui.checkbox("Proie",     self.prey_trajectory)
        #    _, self.pred_trajectory = imgui.checkbox("Predateur", self.pred_trajectory)

        #    imgui.tree_pop()
        """
        imgui.text("Camera lock rotation")
        imgui.new_line()

        imgui.same_line()
        if imgui.button("Proie"):
            self.lookAtTarget = self._proie
        imgui.same_line()
        if imgui.button("Predateur"):
            self.lookAtTarget = self._pret
        imgui.same_line()
        if imgui.button("None"):
            self.lookAtTarget = None
        """
        _, self.selectedCamouflageMode = imgui.combo("Camouflage Mode", self.selectedCamouflageMode, ['Fixed Point', 'Infinit Point', 'Poursuit'])
        _, self.selectedMovementMode = imgui.combo("Movement Mode", self.selectedMovementMode, ['Rectiligne', 'Hélicoïdale', 'Aléatoire'])
        _, self.RESOLUTION           = imgui.input_int("Resolution N", self.RESOLUTION)

        if self.RESOLUTION > 50:  self.RESOLUTION = 50
        elif self.RESOLUTION < 1: self.RESOLUTION = 1

        if len(self.errors):
            imgui.plot_lines("a°", np.array(self.errors, dtype=np.float32), overlay_text=f'avg: {sum(self.errors)/len(self.errors)}', graph_size=(0, 80))
            imgui.plot_lines("Speed", np.array(self.speed, dtype=np.float32), graph_size=(0, 80))
        else:
            imgui.plot_lines("a°", np.array([0], dtype=np.float32), overlay_text="avg: 0", graph_size=(0, 80))
            imgui.plot_lines("Speed", np.array([0], dtype=np.float32), graph_size=(0, 80))

        # _, core.time.Time.GAME_SPEED = imgui.drag_float("Simulation Speed", core.time.Time.GAME_SPEED, 0.01, 0.0, 1.0)


        if imgui.button("Start new simulation"):
            self.startSimulationFunc()


        if imgui.button("Take screen shot"):
            self.takeScreenshotFunction()

        imgui.end()