from OpenGL.GL import *
import numpy as np
import ctypes
import glm

class Espada:
    def __init__(self):
        self.tipo = "espada"
        self.pos = glm.vec3(0.0, 0.0, 0.0)
        self.scale = glm.vec3(0.1, 1.5, 0.1)
        self.color = glm.vec3(0.8, 0.8, 0.8)
        self.size = glm.vec3(abs(self.scale.x), abs(self.scale.y), abs(self.scale.z))

        # Estado da animação
        self.atacando = False
        self.progresso = 0.0
        self.velocidade_estocada = 1.5  # ← você pode ajustar depois

        # Vértices (um cubo fino)
        self.vertices = [
            [-0.5, -0.5, -0.5],
            [ 0.5, -0.5, -0.5],
            [ 0.5,  0.5, -0.5],
            [-0.5,  0.5, -0.5],
            [-0.5, -0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [ 0.5,  0.5,  0.5],
            [-0.5,  0.5,  0.5],
        ]
        self.faces = [
            [4, 5, 6],[6, 7, 4],
            [1, 0, 3],[3, 2, 1],
            [0, 4, 7],[7, 3, 0],
            [5, 1, 2],[2, 6, 5],
            [3, 7, 6],[6, 2, 3],
            [0, 1, 5],[5, 4, 0],
        ]

        # Buffers OpenGL
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vertices = np.array(self.vertices, dtype=np.float32)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))

        self.faces = np.array(self.faces, dtype=np.uint32)
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # -------------------------------
    # Animação de estocada
    # -------------------------------
    def atacar(self):
        """Inicia a animação de estocada."""
        if not self.atacando:
            self.atacando = True
            self.progresso = 0.0

    def update(self, delta_time):
        """Atualiza o progresso da estocada."""
        if self.atacando:
            self.progresso += self.velocidade_estocada * delta_time
            if self.progresso >= 2.0:  # ida (1.0) + volta (1.0)
                self.progresso = 0.0
                self.atacando = False

    def get_offset(self):
        """Calcula o deslocamento da espada durante a estocada."""
        if not self.atacando:
            return 0.0

        # Progresso de 0→1→0 (ida e volta)
        if self.progresso < 1.0:
            return self.progresso  # indo pra frente
        else:
            return 2.0 - self.progresso  # voltando

    # -------------------------------
    # Renderização
    # -------------------------------
    def render(self, shader, jogador_pos, jogador_rot):
        """Renderiza a espada presa à mão do jogador."""
        model = glm.mat4(1.0)

        # Posição base (mão)
        offset = glm.vec3(0.6, 0.0, 0.3)

        # Adiciona deslocamento da estocada
        deslocamento = glm.vec3(0.0, 0.0, +self.get_offset() * 0.8)  # 0.8 é o alcance da estocada
        total_offset = offset + deslocamento

        # Rotaciona offset conforme o jogador
        rotated_offset = glm.rotate(glm.mat4(1.0), jogador_rot, glm.vec3(0, 1, 0)) * glm.vec4(total_offset, 1.0)

        # Matriz final
        model = glm.translate(model, jogador_pos + glm.vec3(rotated_offset))
        model = glm.rotate(model, jogador_rot, glm.vec3(0, 1, 0))  
        model = glm.rotate(model, glm.radians(90), glm.vec3(1, 0, 0))  # Deitar a espada
        model = glm.scale(model, self.scale)

        shader.setMatrix("modelMatrix", glm.value_ptr(model))
        shader.setUniform("color", *self.color)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 3 * len(self.faces), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
