import sys
import time
from core.shader import Shader
from user import User
from drone import Drone
from obstacle import obstacle, loadMap
import cover
from utils.objparser import ObjParser

sys.path.append('py-engine')
sys.path.append('src')

from simulation.simulation import Simulation
from simulation.uavsim import UavSimulation
from simulation.imguiappUAV import ImGuiAppUav

from PIL import Image
from typing import List
from OpenGL.GL import *

#from utils.objparser import ObjParser

from core.primitives import cube, cone, line
import core.components.transform
import core.components.camera
import core.components.cMesh
import core.components.mesh
import core.application
import core.time

import imgui
import glfw
import glm

class GameMultiDrone:

    movementMode   = { 0: 'r', 1: 'h', 2: 'a' }
    camouflageMode = { 0: 'uav' }
    lockCamera: bool = False

    height, width = 50, 50

    m_Application: core.application.Application

    lastX: float = 0
    lastY: float = 0

    mouseInit: bool = False
    cursor   : bool = True

    lines : List[object] = []

    cameraTransform: core.components.transform.Transform

    imGuiApp: ImGuiAppUav
    simulation: Simulation = None

    iteration = 0

    n_users = 100
    non_connected_tr = 10
    non_connected = n_users
    T = 15

    userShader: Shader = None

    def __init__(self) -> None:
        (core.application.Application(init=self.initGame)).run(update=self.update)


    def makeDroneMesh(self):

        droneObject = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj')

        droneObject.m_isActive = False
        return droneObject.getComponent(core.components.cMesh.CMesh)    
    
    def makeConeMesh(self):

        Cone = cone(self.m_Application.m_ActiveScene, (25, 0, 25), 8, (0, 0, 1, .1), [5, 20, 5])
        Cone.m_isActive = False

        return Cone.getComponent(core.components.mesh.Mesh)

    def makeObstacleMesh(self, s):
        obstacle = cube(self.m_Application.m_ActiveScene, (0, 0, 0), (.5, .3, .3, 1), s)

        obstacle.m_isActive = False
        return obstacle.getComponent(core.components.mesh.Mesh)



    def initGame(self, application: core.application.Application):
        self.m_Application = application
        self.m_Application.m_ActiveScene = core.scene.Scene()

        # Creating an entity
        camera_entity = self.m_Application.m_ActiveScene.makeEntity()
        # Giving the entity a transform
        self.cameraTransform = camera_entity.addComponent(core.components.transform.Transform, -15, 10, -10, -20, 20, 20)
        # Adding a camera component
        camera_entity.addComponent(core.components.camera.Camera, 45.0, self.m_Application.WIDTH / self.m_Application.HEIGHT)

        # Setting the input events
        self.m_Application.setOnMouseMove(self.onMouseMove)
        self.m_Application.setProcessInputFunc(self.processInput)

        # Loading the drone objects
        self.ground = cube(self.m_Application.m_ActiveScene, (25, 0, 25), (.3, .3, .3, 1), (self.height, 1, self.width))

        self.droneMesh = self.makeDroneMesh()
        self.obstacleMesh_x = self.makeObstacleMesh((2,2,2))
        self.obstacleMesh_y = self.makeObstacleMesh((4, 20 ,4))
        #self.coneMesh = self.makeConeMesh()

        lines = loadMap('file.txt')
        self.obstacles = []
        

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == 'x' :
                    self.obstacles.append(obstacle(i, j, 1, self.m_Application, self.obstacleMesh_x))
                    
                elif lines[i][j] == 'y' :
                    self.obstacles.append(obstacle(i, j, 10, self.m_Application, self.obstacleMesh_y))
                    

        self.drones    = [Drone(self.m_Application, self.droneMesh, self.obstacles)]
        self.users     = [User(self.height, self.width, self.m_Application, self.obstacles) for _ in range(self.n_users)]
        
        self.initApp()


    def initApp(self):
        self.imGuiApp = ImGuiAppUav()
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
        
        if self.camouflageMode[self.imGuiApp.selectedCamouflageMode] == 'uav' :
            self.simulation = UavSimulation(self.imGuiApp.RESOLUTION)
            
        self.onStartNew()

    def onStartNew(self):
        pass


    def update(self):

        self.imGuiApp.render()

        # imgui.show_test_window()
        if not self.simulation:return
        if not self.simulation.run(): return

        
        # self.mouseInit = False
        # newFront = glm.normalize(glm.vec3(0) - self.cameraTransform.m_Position)
        # self.cameraTransform.front += (newFront - self.cameraTransform.front) * core.time.Time.DELTA_TIME * 10
        # self.cameraTransform.frontToRotation()
        # self.cameraTransform.updateDirectionalVectors()

        self.non_connected = cover.update(self.drones, self.users, self.non_connected_tr, self.m_Application, self.T, self.droneMesh, self.obstacles)
        
        """for user in self.users:
            user.randomWalk(self.iteration, core.time.Time.FIXED_DELTA_TIME

"""     
        for d in self.drones :
            if self.simulation.iteration == 1:
                    
                    d.lastStop = glm.vec3(*d.position)

            if self.simulation.iteration > 1 and self.simulation.iteration % 10 == 0 :
                self.lines.append(line(self.m_Application.m_ActiveScene, d.position,  d.lastStop, d.color))
                
                d.lastStop = glm.vec3(*d.position)

            self.iteration += 1


    
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
        if self.cursor: return

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