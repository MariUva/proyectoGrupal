class Carro:
    def __init__(self):
        self.objetos = []

    def agregar_objeto(self, objeto):
        if objeto.estado == "disponible":
            self.objetos.append(objeto)
            objeto.marcar_reservado()
        else:
            print(f"El objeto {objeto.nombre} no está disponible.")

    def quitar_objeto(self, objeto):
        if objeto in self.objetos:
            self.objetos.remove(objeto)
            objeto.marcar_disponible()

    def listar_objetos(self):
        return [objeto.nombre for objeto in self.objetos]
