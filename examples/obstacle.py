import glm
from regex import R

from core.primitives import cone, cube, line
import core.components.transform
import core.components.camera
import core.components.cMesh
import core.components.mesh
import core.application
import core.time


class obstacle:

    def __init__(self, i, j, app) :
        
        self.position = glm.vec3(1 + i * 2, 1, 1 + j * 2)
        self.obstacleMesh = self.makeObstacleMesh(app)
        self.obstacle = self.generateFromMesh(self.obstacleMesh, self.position, app)
        


    def makeObstacleMesh(self, app):
        obstacle = cube(app.m_ActiveScene, (0, 0, 0), (.5, .3, .3, 1), (2, 2, 2))

        obstacle.m_isActive = False
        return obstacle.getComponent(core.components.mesh.Mesh)


    def generateFromMesh(self, mesh: core.components.mesh.Mesh, position, app):
        obj = app.m_ActiveScene.makeEntity()
        obj.linkComponent(mesh)
        obj.addComponent(core.components.transform.Transform, *position, *([0]*3))

        return obj
    


def loadMap(file):
    with open(file, 'r') as f:
        data = f.readlines()
        
    return data