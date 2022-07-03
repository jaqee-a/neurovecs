
import sys
import time

sys.path.append('py-engine')
sys.path.append('src')

from simulation.simulation import Simulation
from simulation.fixedpoint import FixedPoint
from simulation.infinitpoint import InfinitPoint
from simulation.roadpersue import RoadPursue
from simulation.pursue import Pursue
from simulation.imguiapp import ImGuiApp

from PIL import Image
from typing import List
from OpenGL.GL import *

from utils.objparser import ObjParser

from core.primitives import cube, line, cube2
import core.components.transform
import core.components.camera
import core.application
import core.time

import imgui
import glfw
import glm

class Game:

    movementMode   = { 0: 'r', 1: 'h', 2: 'a' }
    camouflageMode = { 0: 'f', 1: 'i', 2: 'p', 3: 'rp', 4: 'cp', 5: 'uav' }
    selectedMovementMode = 0
    selectedCamouflageMode = 0
    lockCamera: bool = False

    m_Application: core.application.Application

    lastX: float = 0
    lastY: float = 0

    mouseInit: bool = False
    cursor   : bool = True

    lines : List[object] = []

    cameraTransform: core.components.transform.Transform

    imGuiApp: ImGuiApp
    simulation: Simulation = None

    def __init__(self) -> None:
        (core.application.Application(init=self.initGame)).run(update=self.update)

    def makeDroneMesh(self):
        droneObject = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj')

        droneObject.m_isActive = False
        return droneObject.getComponent(core.components.cMesh.CMesh)

    def generateFromMesh(self, mesh: core.components.mesh.Mesh, position):
        obj = self.m_Application.m_ActiveScene.makeEntity()
        obj.linkComponent(mesh)
        obj.addComponent(core.components.transform.Transform, *position, *([0]*3))

        return obj
    def initGame(self, application: core.application.Application):
        self.m_Application = application
        self.m_Application.m_ActiveScene = core.scene.Scene()


        self.droneMesh = self.makeDroneMesh()


        # Creating an entity
        camera_entity = self.m_Application.m_ActiveScene.makeEntity()
        # Giving the entity a transform
        self.cameraTransform = camera_entity.addComponent(core.components.transform.Transform, 0, 0, 5, 0, -90, 0)
        # Adding a camera component
        camera_entity.addComponent(core.components.camera.Camera, 45.0, self.m_Application.WIDTH / self.m_Application.HEIGHT)

        # Setting the input events
        self.m_Application.setOnMouseMove(self.onMouseMove)
        self.m_Application.setProcessInputFunc(self.processInput)

        # Loading the drone objects
        self.preyTransform = self.generateFromMesh(self.droneMesh, (0, 0, 0)).getComponent(core.components.transform.Transform)
        self.predTransform = self.generateFromMesh(self.droneMesh, (0, 0, 0)).getComponent(core.components.transform.Transform)

        self.staticObjects = []

        self.initApp()


    def initApp(self):
        self.imGuiApp = ImGuiApp()
        self.imGuiApp.startSimulationFunc = self.startSimulation
        self.imGuiApp.takeScreenshotFunction = self.takeScreenshot

    def takeScreenshot(self):

        glfw.set_window_size(self.m_Application.m_Window, 4096, 2160)
        glPixelStorei(GL_PACK_ALIGNMENT, 4)
        glReadBuffer(GL_FRONT)
        
        size = glfw.get_framebuffer_size(self.m_Application.m_Window)
        image = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        src = Image.frombuffer('RGBA', size, image).transpose(Image.FLIP_TOP_BOTTOM)
        src.save(f'screenshots/{time.time()}.png')
            


    def clearScene(self):
        for line in self.lines:
            self.m_Application.m_ActiveScene.m_Registry.removeEntity(line)
        
        self.lines.clear()

    def startSimulation(self):
        self.clearScene()

        mode = self.movementMode[self.imGuiApp.selectedMovementMode]
        camMode = self.camouflageMode[self.imGuiApp.selectedCamouflageMode]

        if camMode == 'f' :
            self.simulation = FixedPoint(self.imGuiApp.RESOLUTION, mode)
        elif camMode == 'i' :
            self.simulation = InfinitPoint(self.imGuiApp.RESOLUTION, mode)
        elif camMode == 'p' :
            self.simulation = Pursue(self.imGuiApp.RESOLUTION, mode)
        elif camMode == 'rp' :
            self.simulation = RoadPursue(self.imGuiApp.RESOLUTION, mode, self.m_Application)
        elif camMode == 'cp':
            self.simulation = Checkpoint(self.imGuiApp.RESOLUTION, mode)
        elif camMode == 'uav':
            self.simulation = UavSimulation(self.imGuiApp.RESOLUTION, mode)
        
        self.preyTransform.m_Entity.m_isActive = camMode != 'cp'

        self.selectedCamouflageMode = self.imGuiApp.selectedCamouflageMode
        self.selectedMovementMode = self.imGuiApp.selectedMovementMode

        self.onStartNew()

    def onStartNew(self):
        self.predTransform.m_Position = self.simulation.pred
        
        if self.camouflageMode[self.imGuiApp.selectedCamouflageMode] == 'cp':
            self.imGuiApp.other_plots = [[] for _ in range(len(self.simulation.prey))]
            self.preyTransform.m_Enabled  = False

            for cp in self.simulation.prey:
                self.lines.append(cube(self.m_Application.m_ActiveScene, cp, global_scale=[.2]*3))
        else:
            self.preyTransform.m_Position = self.simulation.prey




    def update(self):
        self.imGuiApp.render()
        # imgui.show_test_window()
        if not self.simulation:return
        if not self.simulation.run(): return

        if self.imGuiApp.cameraLock:
            self.mouseInit = False
            newFront = glm.normalize(self.predTransform.m_Position - self.cameraTransform.m_Position)
            self.cameraTransform.front += (newFront - self.cameraTransform.front) * core.time.Time.DELTA_TIME * 10
            self.cameraTransform.frontToRotation()
            self.cameraTransform.updateDirectionalVectors()

        self.imGuiApp.errors = self.simulation.errors
        self.imGuiApp.speed  = self.simulation.speed

        if self.camouflageMode[self.selectedCamouflageMode] == 'f':
            if self.simulation.iteration == 1:
                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

                self.lines.append(cube(self.m_Application.m_ActiveScene, self.simulation.pred, global_scale=[.1]*3))


            # Line drawing stuff!!
            if self.simulation.iteration > 1 and self.simulation.iteration % 60 == 0 :
                self.lines.append(line(self.m_Application.m_ActiveScene, self.c_lastpos, self.simulation.prey))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.p_lastpos, self.simulation.pred, [1, 0, 0, .3]))
                #self.lines.append(cube(self.m_Application.m_ActiveScene, self.simulation.pred, global_scale=[.1]*3))

                self.lines.append(line(self.m_Application.m_ActiveScene, self.simulation.point, self.simulation.prey, [1, 0, 1, 1]))

                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)
        elif self.camouflageMode[self.selectedCamouflageMode] == 'cp':
            rps = self.simulation.getReferenceVectors()

            for _ in range(len(rps)):
                self.imGuiApp.other_plots = self.simulation.other
                
        elif self.camouflageMode[self.selectedCamouflageMode] == 'uav':
            pass
        
        elif self.camouflageMode[self.selectedCamouflageMode] == 'p' or self.camouflageMode[self.selectedCamouflageMode] == 'rp':

            if self.simulation.iteration == 1:
                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

            if self.simulation.iteration > 1 and self.simulation.iteration % 10 == 0 :
                self.lines.append(line(self.m_Application.m_ActiveScene, self.simulation.prey, self.simulation.pred, [0, 1, 0, .5]))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.c_lastpos, self.simulation.prey, [0, 0, 1, 1]))
                self.lines.append(line(self.m_Application.m_ActiveScene, glm.vec3(self.c_lastpos.x, self.c_lastpos.y+0.02, self.c_lastpos.z), glm.vec3(self.simulation.prey.x, self.simulation.prey.y+0.02, self.simulation.prey.z) , [0, 0, 1, 1]))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.p_lastpos, self.simulation.pred, [1, 0, 0, 1]))
                self.lines.append(line(self.m_Application.m_ActiveScene, glm.vec3(self.p_lastpos.x, self.p_lastpos.y+0.02, self.p_lastpos.z), glm.vec3(self.simulation.pred.x, self.simulation.pred.y+0.02, self.simulation.pred.z) , [1, 0, 0, 1]))

                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

        else:
            if self.simulation.iteration == 1:
                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

            if self.simulation.iteration > 1 and self.simulation.iteration % 60 == 0:
                self.lines.append(line(self.m_Application.m_ActiveScene, self.c_lastpos, self.simulation.prey))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.p_lastpos, self.simulation.pred, [0, 0, 1, .1]))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.simulation.prey, self.simulation.pred, [1, 0, 0, .3]))


                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

        
        """
        if core.time.Time.GAME_SPEED == 0: return



        if self.lookAtTarget != None:
            self.cameraTransform.lookAt(self.lookAtTarget)
        """




    
    def processInput(self, window, activeScene):
        
        if glfw.get_key(window, glfw.KEY_ESCAPE) and imgui.is_key_pressed(256):
            self.cursor = not self.cursor
            glfw.set_input_mode(self.m_Application.m_Window, glfw.CURSOR, glfw.CURSOR_NORMAL if self.cursor else glfw.CURSOR_DISABLED)
            self.mouseInit = False


        if self.cursor: return

        # ll = [*imgui.get_io().keys_down,]
        # if 1 in ll:
        #     print(ll.index)
        
        speed = 5 + (imgui.is_key_down(340) * 25)
        objs = activeScene.m_Registry.getAllOfTypes(core.components.camera.Camera, core.components.transform.Transform)
        # move this code to core
        for entity in objs:
            tr: core.components.transform.Transform = objs[entity][core.components.transform.Transform]
            if glfw.get_key(window, glfw.KEY_D):
                tr.setPosition(*(tr.m_Position + tr.right * core.time.Time.FIXED_DELTA_TIME * speed))

            if glfw.get_key(window, glfw.KEY_A):
                tr.setPosition(*(tr.m_Position - tr.right * core.time.Time.FIXED_DELTA_TIME * speed))

            if glfw.get_key(window, glfw.KEY_S):
                tr.setPosition(*(tr.m_Position - tr.front * core.time.Time.FIXED_DELTA_TIME * speed))

            if glfw.get_key(window, glfw.KEY_W):
                tr.setPosition(*(tr.m_Position + tr.front * core.time.Time.FIXED_DELTA_TIME * speed))

            if glfw.get_key(window, glfw.KEY_LEFT_CONTROL):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, -core.time.Time.FIXED_DELTA_TIME * speed, 0)))

            if glfw.get_key(window, glfw.KEY_SPACE):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, core.time.Time.FIXED_DELTA_TIME * speed, 0)))
            break

    def onMouseMove(self, w, xpos, ypos):
        if self.cursor or self.imGuiApp.cameraLock: return

        if not self.mouseInit:
            self.lastX = xpos
            self.lastY = ypos
            self.mouseInit = True
        
        
        xOffset = xpos - self.lastX
        yOffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 2.0 * core.time.Time.FIXED_DELTA_TIME

        xOffset *= sensitivity
        yOffset *= sensitivity

        self.cameraTransform.rotate(yOffset, xOffset, 0)
        
        if self.cameraTransform.m_Rotation.x > 89.0:
            self.cameraTransform.setPitch(89.0)
        if self.cameraTransform.m_Rotation.x < -89.0:
            self.cameraTransform.setPitch(-89.0)