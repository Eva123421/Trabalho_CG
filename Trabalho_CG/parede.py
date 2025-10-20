from OpenGL.GL import *
import numpy as np
import ctypes
import glm

# Classe Parede
class Parede:
    def __init__(self):
        # Propriedades da parede
        self.pos=glm.vec3(0, 0, 0)
        self.scale=glm.vec3(2, 2, 2)
        self.color=glm.vec3(0.8, 0.2, 0.2)

        # Vértices da parede (um cubo)
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
        #Faces da parede
        self.faces = [
            [4, 5, 6],[6, 7, 4],    # Frente
            [1, 0, 3], [3, 2, 1],   # Trás
            [0, 4, 7],[7, 3, 0],    # Esquerda    
            [5, 1, 2],[2, 6, 5],    # Direita           
            [3, 7, 6],[6, 2, 3],    # Topo         
            [0, 1, 5],[5, 4, 0],    # Base
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

    
    # Colisão AABB com o jogador
    def resolve_collision(self, player):

        # Metade dos tamanhos
        half_player = glm.vec3(0.5, 0.5, 0.5)
        half_wall = self.scale / 2.0

        # Posições mínimas e máximas
        player_min = player.player_pos - half_player
        player_max = player.player_pos + half_player
        wall_min = self.pos - half_wall
        wall_max = self.pos + half_wall

        # Verifica interseção AABB
        overlap_x = min(player_max.x, wall_max.x) - max(player_min.x, wall_min.x)
        overlap_y = min(player_max.y, wall_max.y) - max(player_min.y, wall_min.y)
        overlap_z = min(player_max.z, wall_max.z) - max(player_min.z, wall_min.z)

        if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:
            # Descobre o eixo com menor sobreposição (menos invasão)
            if overlap_y < overlap_x and overlap_y < overlap_z:
                # Corrige no eixo Y (subida/descida)
                if player.player_pos.y > self.pos.y:
                    player.player_pos.y += overlap_y  # em cima da parede
                    player.vel_y = 0
                    player.on_ground = True
                else:
                    player.player_pos.y -= overlap_y  # empurrado por baixo
                    player.vel_y = 0
            elif overlap_x < overlap_z:
                # Corrige no eixo X (lateral)
                if player.player_pos.x > self.pos.x:
                    player.player_pos.x += overlap_x
                else:
                    player.player_pos.x -= overlap_x
            else:
                # Corrige no eixo Z (frente/trás)
                if player.player_pos.z > self.pos.z:
                    player.player_pos.z += overlap_z
                else:
                    player.player_pos.z -= overlap_z
    
    #render da parede
    def render(self, shader):
        model = glm.mat4(1.0)
        model = glm.translate(model, self.pos)
        model = glm.scale(model, self.scale)
        shader.setMatrix("modelMatrix", glm.value_ptr(model))
        shader.setUniform("color", *self.color)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 3*len(self.faces), GL_UNSIGNED_INT, None)
