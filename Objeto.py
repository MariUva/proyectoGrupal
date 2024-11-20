class Objeto:
    def __init__(self, id_objeto, nombre, descripcion, estado="disponible"):
        self.id_objeto = id_objeto
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado  # disponible, reservado, prestado

    def marcar_reservado(self):
        self.estado = "reservado"

    def marcar_prestado(self):
        self.estado = "prestado"

    def marcar_disponible(self):
        self.estado = "disponible"
