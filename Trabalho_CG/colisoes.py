import glm

class Colisoes:
    def __init__(self):
        # Lista de todos os objetos que participam das colisões
        self.objetos = []

    def registrar(self, objeto):
        """
        Adiciona um objeto à lista de colisões.
        Cada objeto deve ter:
        - pos: glm.vec3 (posição central)
        - size: glm.vec3 (largura, altura, profundidade)
        - método ao_colidir(outro)
        """
        self.objetos.append(objeto)

    def remover(self, objeto):
        #Remove um objeto da lista de colisões (se for destruído, por exemplo)
        if objeto in self.objetos:
            self.objetos.remove(objeto)

    def verificar_colisoes(self):
        """
        Verifica colisões entre todos os pares de objetos registrados.
        Chama o método ao_colidir() de ambos os objetos quando ocorre colisão.
        """
        for i in range(len(self.objetos)):
            for j in range(i + 1, len(self.objetos)):
                a = self.objetos[i]
                b = self.objetos[j]

                if self._colidem(a, b):
                    a.ao_colidir(b)
                    b.ao_colidir(a)

    def _colidem(self, a, b):
        """
        Verifica colisão simples de caixas AABB (Axis-Aligned Bounding Box).
        Usa posição central (pos) e tamanho (size) de cada objeto.
        """
        return (
            abs(a.pos.x - b.pos.x) * 2 < (a.size.x + b.size.x) and
            abs(a.pos.y - b.pos.y) * 2 < (a.size.y + b.size.y) and
            abs(a.pos.z - b.pos.z) * 2 < (a.size.z + b.size.z)
        )
