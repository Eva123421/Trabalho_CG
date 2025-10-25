from OpenGL.GL import *
import numpy as np
import ctypes
import glm
from shader import Shader
class Chao:
    def __init__(self):
        #parâmetros do chão
        self.pos = glm.vec3(0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.size = glm.vec3(abs(self.scale.x), 
                             abs(self.scale.y), 
                             abs(self.scale.z))

        self.color = glm.vec3(0.1, 0.8, 0.1)
        # vértices do chão
        self.vertices = [
            [-10.0, 0.0, -10.0],
            [10.0, 0.0, -10.0],
            [10.0, 0.0,  10.0],
            [-10.0, 0.0,  10.0]
        ]
        # faces do chão
        self.faces = [
            [0, 1, 2],
            [2, 3, 0]
        ]

        self.vertices = np.array(self.vertices,dtype = np.float32)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        self.faces = np.array(self.faces, dtype = np.uint32)
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindVertexArray(0)


    # renderiza o chão
    def render(self, shader):
        model = glm.mat4(1.0)
        model = glm.translate(model, self.pos)
        model = glm.scale(model, self.scale)
        shader.setMatrix("modelMatrix", glm.value_ptr(model))  # padronizado
        shader.setUniform("color", 0.1, 0.8, 0.1)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.faces)*3, GL_UNSIGNED_INT, None)
