class GestorDePrestamos:
    def __init__(self):
        self.solicitudes = []

    def crear_solicitud(self, cliente, objetos):
        id_solicitud = len(self.solicitudes) + 1
        solicitud = {"id": id_solicitud, "cliente": cliente, "objetos": objetos}
        self.solicitudes.append(solicitud)
        return solicitud
