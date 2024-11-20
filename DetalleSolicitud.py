from ConexionBD import ConexionDB


class DetalleSolicitud:
    def __init__(self, id_detalle, id_solicitud, id_objeto):
        self.id_detalle = id_detalle
        self.id_solicitud = id_solicitud
        self.id_objeto = id_objeto

    @staticmethod
    def agregar(id_solicitud, id_objeto):
        """Agrega un detalle de solicitud"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        query = "INSERT INTO Detalle_Solicitud (id_solicitud, id_objeto) VALUES (%s, %s)"
        values = (id_solicitud, id_objeto)
        cursor.execute(query, values)
        conexion.connection.commit()
        conexion.cerrar()
