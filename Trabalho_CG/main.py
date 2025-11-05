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
from espada import Espada

# Variáveis globais
width, height = 800, 600
jogador = None
espada = None
chao = None
myShader = None
colisoes = Colisoes()
window = None
parede_model = None
rampa_model = None
paredes_transform = []
rampas_transform = []
botao_esquerdo_pressionado = False
botao_direito_pressionado = False






def init():
    global myShader, jogador, espada, chao, rampas, rampa_model, rampas_transform, parede_model, paredes_transform

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
    scale = 1.0
    jogador.scale = glm.vec3(scale, scale, scale) 
    jogador.atualizar_tamanho()

    # Cria espada
    espada = Espada()
    



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

    rampa_model = Rampa()
    rampas_transform = [
        {
            "pos": glm.vec3(-7, 0.01, -3.99),
            "scale": glm.vec3(4, 6, 8),
            "rotation_y": 0.0,
            "color": (0.2, 0.2, 0.2)
        }
    ]


    #Criar Paredes
    parede_model = Parede()
    paredes_transform = [
        {"pos": glm.vec3(-5, altura_parede_pos, -8), "scale": glm.vec3(6, altura_parede_tamanho, 8)},
        {"pos": glm.vec3(-10.01, altura_parede_pos, -2), "scale": glm.vec3(6, altura_parede_tamanho, 20)},
        {"pos": glm.vec3(0.01, altura_parede_pos, -2.0), "scale": glm.vec3(6, altura_parede_tamanho, 20)},
    ]
    # 🔹 Informa ao sistema de colisões as instâncias existentes
    colisoes.definir_instancias("parede", paredes_transform)
    colisoes.definir_instancias("rampa", rampas_transform)
    # Passa as paredes pro jogador
    
    
    # Registra todos que devem colidir
    colisoes.registrar(jogador)
    colisoes.registrar(chao)
    colisoes.registrar(rampa_model)
    colisoes.registrar(parede_model)

    

# Processa entrada do teclado
def process_input(window, delta_time):
    global botao_esquerdo_pressionado, botao_direito_pressionado
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
        jogador.move(move_dir, delta_time, rampa_model)
    # --- ATAQUES COM CLIQUE ÚNICO ---
    # Botão esquerdo → estocada
    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        if not botao_esquerdo_pressionado:  # só dispara uma vez
            espada.atacar_estocada()
            botao_esquerdo_pressionado = True
    else:
        botao_esquerdo_pressionado = False

    # Botão direito → corte
    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS:
        if not botao_direito_pressionado:  # só dispara uma vez
            espada.atacar_corte()
            botao_direito_pressionado = True
    else:
        botao_direito_pressionado = False



# Renderiza a cena
def render():
    global myShader, jogador, chao
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    myShader.bind()

    # Atualiza câmera antes de desenhar
    jogador.update_cam(myShader)

    # Renderiza jogador
    jogador.render(myShader)
    # Espada (acoplada ao jogador)
    espada.render(myShader, jogador.pos, jogador.rotation_y)


    # Renderiza chão
    chao.render(myShader)

    # Renderiza rampas
    for r in rampas_transform:
        rampa_model.render(myShader, r["pos"], 
                           r["scale"], 
                           r["rotation_y"], 
                           r["color"])
    # Renderiza paredes
    for p in paredes_transform:
        parede_model.render(myShader, 
                            p["pos"], 
                            p["scale"])
    
    colisoes.verificar_colisoes(jogador)

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
        jogador.update(delta_time, rampa_model, rampas_transform)
        espada.update(delta_time)

        
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
