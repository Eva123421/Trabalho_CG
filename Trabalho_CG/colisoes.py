import glm

class Colisoes:
    def __init__(self):
        self.objetos = []

    def registrar(self, objeto):
        """
        Cada objeto precisa ter:
        - pos: glm.vec3 (posição)
        - size: glm.vec3 (dimensões)
        - tipo: string ('jogador', 'parede', 'chao', 'rampa', etc)
        - método ao_colidir(outro)
        """
        self.objetos.append(objeto)

    def remover(self, objeto):
        if objeto in self.objetos:
            self.objetos.remove(objeto)

    def verificar_colisoes(self):
        for i in range(len(self.objetos)):
            for j in range(i + 1, len(self.objetos)):
                a = self.objetos[i]
                b = self.objetos[j]

                # 🔹 Ignora colisões entre objetos estáticos (cenário)
                if a.tipo != "jogador" and b.tipo != "jogador":
                    continue

                if self._colidem(a, b):
                    a.ao_colidir(b)
                    b.ao_colidir(a)

    def _colidem(self, a, b):
        """Colisão AABB (Axis-Aligned Bounding Box)"""
        return (
            abs(a.pos.x - b.pos.x) * 2 < (a.size.x + b.size.x) and
            abs(a.pos.y - b.pos.y) * 2 < (a.size.y + b.size.y) and
            abs(a.pos.z - b.pos.z) * 2 < (a.size.z + b.size.z)
        )
