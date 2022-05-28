from typing import List

import numpy as np
import imgui

class ImGuiAppUav:
    selectedCamouflageMode: int = 0

    other_plots: List[List[float]] = []
    RESOLUTION: int     = 4

    def __init__(self) -> None:
        pass

    def startSimulationFunc(self):
        pass

    def takeScreenshotFunction(self):
        pass

    def render(self):
        imgui.begin("Control Panel", True)

        _, self.selectedCamouflageMode = imgui.combo("Camouflage Mode", self.selectedCamouflageMode, ['Uav Simulation'])
        _, self.RESOLUTION             = imgui.input_int("Resolution N", self.RESOLUTION)

        if self.RESOLUTION > 50:  self.RESOLUTION = 50
        elif self.RESOLUTION < 1: self.RESOLUTION = 1

        for plot in self.other_plots:
            if len(plot):
                imgui.plot_lines("PLT", np.array(plot, dtype=np.float32), scale_min=0, scale_max=500, graph_size=(0, 80))
            else:
                imgui.plot_lines("PLT", np.array([0], dtype=np.float32), graph_size=(0, 80))

        # _, core.time.Time.GAME_SPEED = imgui.drag_float("Simulation Speed", core.time.Time.GAME_SPEED, 0.01, 0.0, 1.0)


        if imgui.button("Start new simulation"):
            self.startSimulationFunc()


        if imgui.button("Take screen shot"):
            self.takeScreenshotFunction()

        imgui.end()