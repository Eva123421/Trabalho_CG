from OpenGL.GL import *
import numpy as np
import ctypes
import glm  



class Jogador:
    def __init__(self):
        # Propriedades do jogador
        self.pos = glm.vec3(7.0, 0.5, 7.0)
        self.rotate = 0.0
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.size = glm.vec3(abs(self.scale.x), 
                             abs(self.scale.y), 
                             abs(self.scale.z))
        self.color = glm.vec3(0.0, 0.5, 1.0)
        self.WIDTH = 800
        self.HEIGHT = 600
        self.camera_angle = glm.radians(0.0)
        self.camera_height = 6.0
        self.camera_distance = 8.0
        self.rotation_y = 0.0  
        self.vel_y = 0.0
        self.on_ground = True


        # vértices do cubo(jogador)
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
        #Faces do cubo(jogador)
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



    # Atualiza posição da câmera com base na posição do jogador
    def update_cam(self, shader):
        # A câmera orbita o jogador no plano XZ
        cam_x = self.pos.x + self.camera_distance * glm.sin(self.camera_angle)# deslocamento horizontal (eixo X) da câmera
        cam_z = self.pos.z + self.camera_distance * glm.cos(self.camera_angle) # deslocamento horizontal (eixo Z) da câmera

        # Y representa a altura da câmera em relação ao jogador
        target_y = self.pos.y + 5.0  # altura desejada da câmera (acima do jogador)
        self.camera_height += (target_y - self.camera_height) * 0.1  # suaviza o movimento vertical da câmera
        cam_y = self.camera_height  # define a altura final da câmera

        # Posição final da câmera
        camera_pos = glm.vec3(cam_x, cam_y, cam_z)

        # Cria a matriz de visualização (view matrix)
        # Define a posição da câmera, o ponto para onde ela olha (jogador) e o eixo "para cima" (Y)
        view = glm.lookAt(camera_pos,   # posição da câmera no mundo
                        self.pos,  # ponto que a câmera está olhando (alvo)
                        glm.vec3(0, 1, 0))  # vetor 'up' indicando que o eixo Y é o eixo vertical


        # Configura a projeção em perspectiva: define o campo de visão, proporção da tela e limites de renderização
        projection = glm.perspective(glm.radians(45.0),  # campo de visão (FOV) de 45 graus
                                    self.WIDTH / self.HEIGHT,  # razão de aspecto da janela
                                    0.1,  # plano de recorte próximo (near plane)
                                    100.0)  # plano de recorte distante (far plane)


        # Envia as matrizes de visualização e projeção para o shader
        shader.setMatrix("viewMatrix", glm.value_ptr(view))
        shader.setMatrix("projectionMatrix", glm.value_ptr(projection))



    #move o jogador com base na entrada do teclado
    def move(self, direction, delta_time, rampas=[]):
        speed = 5.0
        # mover o jogador na direção X
        right = glm.normalize(glm.vec3(glm.cos(self.camera_angle), 0, glm.sin(self.camera_angle)))
        # mover o jogador na direção Z
        forward = glm.normalize(glm.cross(right, glm.vec3(0, 1, 0)))
        
        move_vec = glm.vec3(0)  # vetor de movimento inicial (sem direção)

        # Define a direção do movimento conforme a tecla pressionada
        if direction == 'up':
            move_vec -= forward
        elif direction == 'down':
            move_vec += forward
        elif direction == 'left':
            move_vec -= right
        elif direction == 'right':
            move_vec += right

        # Aplica o movimento e atualiza a rotação do jogador
        if glm.length(move_vec) > 0:
            move_vec = glm.normalize(move_vec)  # garante velocidade constante em qualquer direção
            self.pos += move_vec * speed * delta_time  # desloca o jogador
            self.rotation_y = glm.atan(move_vec.x, move_vec.z)  # gira o jogador na direção do movimento



    # Atualiza o jogador (gravidade, colisões, etc)
    def update(self, delta_time, rampas=[]):
        gravity = -15.0
        self.vel_y += gravity * delta_time  # aplica gravidade

        # Aplica movimento vertical
        self.pos.y += self.vel_y * delta_time

        # ajusta a altura do jogador com base no chão e rampas
        altura_chao = 0.5
        altura_base_jogador = altura_chao + 0.5

        # Detecta altura da rampa em que o jogador está
        altura_rampa = None
        for rampa in rampas:
            h = rampa.get_height_at(self.pos.x, self.pos.z)
            if h is not None:
                altura_rampa = h
                break

        # Define a altura alvo: usa a da rampa se estiver sobre uma, senão usa a do chão
        altura_alvo = altura_rampa + 0.5 if altura_rampa is not None else altura_base_jogador


        # Impede atravessar o chão/rampa
        if self.pos.y <= altura_alvo:
            self.pos.y = altura_alvo
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        



    # Renderiza o jogador
    def render(self, shader):
            
            glBindVertexArray(self.vao)

            # Cor e matriz modelo
            shader.setUniform("color", self.color.x, self.color.y, self.color.z)
            model = glm.mat4(1.0)
            model = glm.translate(model, self.pos)
            model = glm.rotate(model, self.rotation_y, glm.vec3(0, 1, 0))  # usa rotação Y real
            model = glm.scale(model, self.scale)

            shader.setMatrix("modelMatrix", glm.value_ptr(model))
            glDrawElements(GL_TRIANGLES, 3*len(self.faces), GL_UNSIGNED_INT, None)

            glBindVertexArray(0)
            
