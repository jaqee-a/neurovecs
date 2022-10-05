import glm

from core.primitives import cone, cube, line
import core.components.transform
import core.components.camera
import core.components.cMesh
import core.components.mesh
import core.application
import core.time


class obstacle:

    def __init__(self, i, j, h, app, mesh, type) :

        self.m_app = app
        
        self.position = glm.vec3(6 + i * 12, h, 6 + j * 12)
        self.obstacle = self.generateFromMesh(mesh, self.position, app)
        
        self.type = type


    def generateFromMesh(self, mesh: core.components.mesh.Mesh, position, app) :
        obj = app.m_ActiveScene.makeEntity()
        obj.linkComponent(mesh)
        obj.addComponent(core.components.transform.Transform, *position, *([0]*3))

        return obj

    def destroy(self) :
        self.m_app.m_ActiveScene.m_Registry.removeEntity(self.obstacle)
    


def loadMap(file):
    with open(file, 'r') as f:
        data = f.readlines()
        
    return data