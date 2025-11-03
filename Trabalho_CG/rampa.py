from OpenGL.GL import *
import numpy as np
import ctypes
import glm


class Rampa:
    def __init__(self, direction='z+'):
        # Propriedades da rampa
        self.tipo = "rampa"
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
    def get_height_at(self, x, z, pos=None, scale=None, rotation_y=0.0):
        """
        Calcula a altura do ponto (x, z) no espaço da rampa.
        Se pos, scale e rotation_y forem fornecidos, usa os da instância.
        """

        pos = pos or self.pos
        scale = scale or self.scale

        # Constrói a matriz de transformação completa da instância
        model = glm.mat4(1.0)
        model = glm.translate(model, pos)
        model = glm.rotate(model, glm.radians(rotation_y), glm.vec3(0, 1, 0))
        model = glm.scale(model, scale)

        # Calcula a inversa para converter coordenadas do mundo -> local
        inv_model = glm.inverse(model)

        local_point = inv_model * glm.vec4(x, 0.0, z, 1.0)
        lx, lz = local_point.x, local_point.z

        # Verifica se o ponto está dentro dos limites da rampa local (0..1)
        if not (0.0 <= lx <= 1.0 and 0.0 <= lz <= 1.0):
            return None

        # Calcula progresso na inclinação
        if self.direction == 'z+':
            progress = 1.0 - lz
        else:
            progress = 1.0 - lx

        # Altura local proporcional
        height_local = progress * 1.0  # de 0 até 1
        height_world = pos.y + (height_local * scale.y)
        return height_world

    def atualizar_tamanho(self):
        self.size = glm.vec3(abs(self.scale.x), abs(self.scale.y), abs(self.scale.z))

    def ao_colidir(self, outro):
        pass

    # Renderiza a rampa
    def render(self, shader, pos, scale, rotation_y=0.0, color=None):
        shader.setUniform("color", *(color if color else self.color))
        model = glm.mat4(1.0)
        model = glm.translate(model, pos)
        model = glm.rotate(model, glm.radians(rotation_y), glm.vec3(0, 1, 0))
        model = glm.scale(model, scale)
        shader.setMatrix("modelMatrix", glm.value_ptr(model))
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 3 * len(self.faces), GL_UNSIGNED_INT, None)


    