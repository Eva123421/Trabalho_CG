import glfw
from OpenGL.GL import *
import os
import glm
from shader import Shader
from jogador import Jogador
from chao import Chao
from rampa import Rampa
from parede import Parede
from colisoes import Colisoes



# Variáveis globais
width, height = 800, 600
jogador = None
chao = None
myShader = None
colisoes = Colisoes()
rampas = []
paredes = []
window = None


def init():
    global myShader, jogador, chao, rampas

    glClearColor(0.9, 0.9, 0.9, 1)
    glEnable(GL_DEPTH_TEST)

    # Carrega shader
    myShader = Shader(
        os.path.join(os.path.dirname(__file__), "vertex.glsl"),
        os.path.join(os.path.dirname(__file__), "fragment.glsl")
    )

    # Cria jogador
    # Cria o gerenciador global de colisõesa
    jogador = Jogador()
    jogador.atualizar_tamanho()



    #------------------
    #Criação do cenário
    #------------------
    altura_parede_tamanho = 6.0
    altura_parede_pos = altura_parede_tamanho / 2.00
     
    # Cria chão 
    chao = Chao()
    chao.pos = glm.vec3(0, 0, 0)
    chao.scale = glm.vec3(10, 1, 10)
    chao.atualizar_tamanho()
    
    # Cria rampas

    
    rampa1 = Rampa()
    rampa1.pos = glm.vec3(-7, 0.01, -3.99)
    rampa1.scale = glm.vec3(4, 6, 8)
    rampa1.rotation_y = 0.0  
    rampa1.color = (0.2, 0.2, 0.2)
    rampa1.atualizar_tamanho()
    rampas.append(rampa1)

    #Criar Paredes
    
    

    parede1 = Parede()
    parede1.pos = glm.vec3(-5, altura_parede_pos, -8)
    parede1.scale = glm.vec3(6, altura_parede_tamanho, 8)
    parede1.atualizar_tamanho()
    paredes.append(parede1)

    parede2 = Parede()
    parede2.pos = glm.vec3(-10.01, altura_parede_pos, -2)
    parede2.scale = glm.vec3(6, altura_parede_tamanho, 20)
    parede2.atualizar_tamanho()
    paredes.append(parede2)

    parede3 = Parede()
    parede3.pos = glm.vec3(0.01, altura_parede_pos, -2.0)
    parede3.scale = glm.vec3(6, altura_parede_tamanho, 20)
    parede3.atualizar_tamanho()
    paredes.append(parede3)

    # Passa as paredes pro jogador
    jogador.paredes = paredes
    

    # Registra todos que devem colidir
    colisoes.registrar(jogador)
    colisoes.registrar(chao)
    colisoes.registrar(rampa1)
    for parede in paredes:
        colisoes.registrar(parede)

    

# Processa entrada do teclado
def process_input(window, delta_time):
    move_dir = None
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        move_dir = 'up'
    elif glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        move_dir = 'down'
    elif glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        move_dir = 'left'
    elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        move_dir = 'right'

    if move_dir:
        jogador.move(move_dir, delta_time, rampas)

# Renderiza a cena
def render():
    global myShader, jogador, chao, rampas
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    myShader.bind()

    # Atualiza câmera antes de desenhar
    jogador.update_cam(myShader)

    # Renderiza jogador
    jogador.render(myShader)

    # Renderiza chão
    chao.render(myShader)

    # Renderiza rampas
    for r in rampas:
        r.render(myShader)
    
    # Renderiza paredes
    for p in paredes:
        p.render(myShader)
    colisoes.verificar_colisoes()




    myShader.unbind()



# Função principal
def main():
    global window
    if not glfw.init():
        return
    #Cria a janela
    window = glfw.create_window(width, height, "Subida realista em rampas", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    init()

    last_time = glfw.get_time()
    # Loop principal
    while not glfw.window_should_close(window):
        # Calcula delta time
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        glfw.poll_events()
        process_input(window, delta_time)
        jogador.update(delta_time, rampas)
        
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
