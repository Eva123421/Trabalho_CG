from OpenGL.GL import *
import numpy as np
import ctypes
import glm


class Rampa:
    def __init__(self, direction='z+'):
        # Propriedades da rampa
        self.pos=glm.vec3(0,0,0)
        self.scale=glm.vec3(4,2,4)
        self.size = glm.vec3(abs(self.scale.x), 
                             abs(self.scale.y), 
                             abs(self.scale.z))

        self.direction = direction
        self.rotation_y = 0.0  # em graus
        self.color = glm.vec3(0.8, 0.3, 0.1)

        # Vértices da rampa
        self.vertices = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],  # inclinação
            [0.0, 0.0, 1.0]
        ]
        # Faces da rampa
        self.faces = [
            [0, 1, 2], [2, 3, 0],  # base
            [0, 1, 5], [5, 4, 0],  # topo
            [1, 2, 6], [6, 5, 1],  # lado direito
            [0, 3, 7], [7, 4, 0],  # lado esquerdo
            [2, 3, 7], [7, 6, 2],  # lado de trás
            [3, 0, 4], [4, 7, 3]   # lado da frente
        ]

        # Buffers OpenGL
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

            # Criando VBO
        self.vertices = np.array(self.vertices, dtype=np.float32)
        vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboId)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3*4, ctypes.c_void_p(0))

        # Criando EBO
        self.faces = np.array(self.faces, dtype=np.uint32)
        eboId = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboId)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Calcula altura levando em conta rotação e escala
    def get_height_at(self, x, z):
        # Inverter as transformações do modelo (trazer o ponto pro espaço local)
        model = glm.mat4(1.0)
        model = glm.translate(model, self.pos)
        model = glm.rotate(model, glm.radians(self.rotation_y), glm.vec3(0, 1, 0))
        model = glm.scale(model, self.scale)

        # Matriz inversa (mundo → local)
        inv_model = glm.inverse(model)

        # Transforma o ponto do jogador para o espaço local da rampa
        local_point = inv_model * glm.vec4(x, 0.0, z, 1.0)

        lx, lz = local_point.x, local_point.z

        # A rampa vai de 0→1 em X e Z no espaço local
        if not (0.0 <= lx <= 1.0 and 0.0 <= lz <= 1.0):
            return None

        # Altura proporcional dentro da rampa
        if self.direction == 'z+':
            progress = 1.0 - lz
        else:
            progress = 1.0 - lx


        height_local = progress * 1.0  # altura vai até 1 no espaço local
        height_world = self.pos.y + (height_local * self.scale.y)
        return height_world

    # Renderiza a rampa
    def render(self, shader):
        shader.setUniform("color", *self.color)
        model = glm.mat4(1.0)
        model = glm.translate(model, self.pos)
        model = glm.rotate(model, glm.radians(self.rotation_y), glm.vec3(0, 1, 0))
        model = glm.scale(model, self.scale)

        shader.setMatrix("modelMatrix", glm.value_ptr(model))
        

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 3*len(self.faces), GL_UNSIGNED_INT, None)

    