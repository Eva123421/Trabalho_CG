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

        # Estados de animação
        self.atacando_estocada = False
        self.atacando_corte = False
        self.progresso = 0.0
<<<<<<< Updated upstream
        self.velocidade_estocada = 6  # ← você pode ajustar depois
=======
        self.velocidade_estocada = 1.5
        self.velocidade_corte = 2.0
>>>>>>> Stashed changes

        # Vértices (cubo fino)
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
    # Controle de ataques
    # -------------------------------
    def atacar_estocada(self):
        if not self.atacando_estocada and not self.atacando_corte:
            self.atacando_estocada = True
            self.progresso = 0.0

    def atacar_corte(self):
        if not self.atacando_estocada and not self.atacando_corte:
            self.atacando_corte = True
            self.progresso = 0.0

    def update(self, delta_time):
        if self.atacando_estocada:
            self.progresso += self.velocidade_estocada * delta_time
            if self.progresso >= 2.0:
                self.progresso = 0.0
                self.atacando_estocada = False

        elif self.atacando_corte:
            self.progresso += self.velocidade_corte * delta_time
            if self.progresso >= 2.0:
                self.progresso = 0.0
                self.atacando_corte = False

    # -------------------------------
    # Movimentos das animações
    # -------------------------------
    def get_offset_estocada(self):
        if not self.atacando_estocada:
            return 0.0
        return self.progresso if self.progresso < 1.0 else 2.0 - self.progresso

    def get_angulo_corte(self):
        if not self.atacando_corte:
            return 0.0
        # vai de -90° a +90° e volta
        if self.progresso < 1.0:
            return -90 + 180 * self.progresso
        else:
            return 90 - 180 * (self.progresso - 1.0)

    # -------------------------------
    # Renderização
    # -------------------------------
    def render(self, shader, jogador_pos, jogador_rot):
        model = glm.mat4(1.0)
        # --- offset da espada na mão ---
        offset = glm.vec3(0.6, 0.0, 0.3)
        deslocamento = glm.vec3(0.0, 0.0, +self.get_offset_estocada() * 0.8)
        total_offset = offset + deslocamento
        rotated_offset = glm.rotate(glm.mat4(1.0), jogador_rot, glm.vec3(0, 1, 0)) * glm.vec4(total_offset, 1.0)

        # --- deslocamento lateral fixo no espaço local do jogador ---
        offset_local = glm.vec3(-0.4, 0.0, 0.9)  # 0.5 à direita
        offset_rotacionado = glm.rotate(glm.mat4(1.0), jogador_rot, glm.vec3(0, 1, 0)) * glm.vec4(offset_local, 1.0)
        pos_ajustada = jogador_pos + glm.vec3(offset_rotacionado)

        # --- aplica tudo ---
        model = glm.translate(model, pos_ajustada + glm.vec3(rotated_offset))
        model = glm.rotate(model, jogador_rot, glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(90), glm.vec3(1, 0, 0))


        # ------------------------------------------------------
        # PIVÔ DE ROTAÇÃO NA BASE (corte horizontal)
        # ------------------------------------------------------
        if self.atacando_corte:
            angulo = self.get_angulo_corte()
            # Move pivô para base (parte inferior da espada)
            # Como a escala Y define o comprimento da espada,
            # movemos -0.5 na direção do eixo Y antes de girar.
            model = glm.translate(model, glm.vec3(0, -0.5, 0))
            model = glm.rotate(model, glm.radians(angulo), glm.vec3(0, 0, 1))
            model = glm.translate(model, glm.vec3(0, +0.5, 0))

        # Escala final
        model = glm.scale(model, self.scale)

        shader.setMatrix("modelMatrix", glm.value_ptr(model))
        shader.setUniform("color", *self.color)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 3 * len(self.faces), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
