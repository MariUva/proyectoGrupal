class Solicitud:
    def __init__(self, id_solicitud, cliente, objetos):
        self.id_solicitud = id_solicitud
        self.cliente = cliente
        self.objetos = objetos  # lista de objetos solicitados
        self.aprobada = False

    def aprobar(self):
        self.aprobada = True

    def rechazar(self):
        self.aprobada = False
