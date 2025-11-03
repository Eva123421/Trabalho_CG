import glm

class Colisoes:
    def __init__(self):
        self.objetos = []
        self.transforms = {}  # mapeia tipo -> lista de transformações (paredes, rampas etc.)

    def registrar(self, objeto):
        """Registra objetos e guarda os modelos repetíveis (parede/rampa)."""
        self.objetos.append(objeto)

    def definir_instancias(self, tipo, lista_transforms):
        """Define transformações (pos, scale, rotation_y, etc.) para um tipo de objeto."""
        self.transforms[tipo] = lista_transforms

    def remover(self, objeto):
        if objeto in self.objetos:
            self.objetos.remove(objeto)

    def verificar_colisoes(self, jogador):
        for obj in self.objetos:
            # Ignora o próprio jogador
            if obj.tipo == "jogador":
                continue

            # 🔹 Se for um tipo com várias instâncias (ex: parede/rampa)
            if obj.tipo in self.transforms:
                for t in self.transforms[obj.tipo]:
                    if self._colidem(jogador, obj, t["pos"], t["scale"]):
                        jogador.ao_colidir(self._dummy(obj.tipo, t["pos"], t["scale"]))
            else:
                # 🔹 Objetos únicos (como chão)
                if self._colidem(jogador, obj, obj.pos, obj.scale):
                    jogador.ao_colidir(obj)

    def _colidem(self, a, b_model, b_pos, b_scale):
        """Colisão AABB (Axis-Aligned Bounding Box) com transformações."""
        a_min = a.pos - a.size / 2.0
        a_max = a.pos + a.size / 2.0

        b_size = glm.vec3(abs(b_scale.x), abs(b_scale.y), abs(b_scale.z))
        b_min = b_pos - b_size / 2.0
        b_max = b_pos + b_size / 2.0

        return (
            a_min.x <= b_max.x and a_max.x >= b_min.x and
            a_min.y <= b_max.y and a_max.y >= b_min.y and
            a_min.z <= b_max.z and a_max.z >= b_min.z
        )

    def _dummy(self, tipo, pos, scale):
        """Cria um objeto leve só com tipo, pos e tamanho para repassar ao jogador."""
        d = type("Dummy", (), {})()
        d.tipo = tipo
        d.pos = pos
        d.scale = scale
        d.size = glm.vec3(abs(scale.x), abs(scale.y), abs(scale.z))
        return d
