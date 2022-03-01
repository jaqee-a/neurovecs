import numpy as np
import core.time
import glm



class Simulation:


    def __init__(self, resolution: int, type_: str) -> None:
        self.resolution = resolution
        self.type  = type_
        
        self.mv_vec = glm.normalize(glm.vec3(np.random.random() ,np.random.random(),np.random.random())) * 10 * core.time.Time.FIXED_DELTA_TIME

        if self.type == 'r' :
            self.prey  = glm.vec3(np.random.random()*40,np.random.random()*40,np.random.random()*40)

        elif self.type == 'h' :
            self.prey = glm.vec3(np.cos(0), 0, np.sin(0))

        elif self.type == 'a' :
            self.prey = glm.vec3(15, 0, 0)
            self.v = glm.vec3(0, .01, .01)

        self.point = glm.vec3(0)
        self.pred  = glm.vec3(0)

        # Speed
        self.alpha = 0.0054

        self.errors = []
        self.speed  = []

        self.iteration = -1

    def simulationOver(self):
        return glm.distance(self.prey, self.pred) < .3

    def updatePreyPosition(self):
        # Movement rectiligne
        if self.type == 'r':
            self.prey += self.mv_vec#glm.vec3(0, core.time.Time.FIXED_DELTA_TIME, 0)
        # Movement helicoidale 
        if self.type == 'h':
            self.prey.x = 5 * np.cos(np.radians(self.iteration))
            self.prey.y = self.iteration * core.time.Time.FIXED_DELTA_TIME
            self.prey.z = 5 * np.sin(np.radians(self.iteration))
        # Movement Aleatoire
        if self.type == 'a' :
            self.prey += self.v
            if self.iteration % 10 == 0 :
                axis = [glm.vec3(1, 0, 0), glm.vec3(0, 1, 0), glm.vec3(0, 0, 1)]
                np.random.shuffle(axis)
                self.v = glm.rotate(self.v, np.pi/9, axis[0])



    def run(self):
        self.iteration += 1

    def getReferenceVectors(self):
        pass

    def getError(self):
        pass