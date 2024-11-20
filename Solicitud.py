class Solicitud:
    def __init__(self, id_solicitud, id_cliente, fecha_prestamo, fecha_devolucion, aprobada):
        self.id_solicitud = id_solicitud
        self.id_cliente = id_cliente
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.aprobada = aprobada

    @staticmethod
    def obtener_todas():
        """Obtiene todas las solicitudes"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT * FROM Solicitudes")
        solicitudes = cursor.fetchall()
        conexion.cerrar()

        return [Solicitud(id_solicitud=s[0], id_cliente=s[1], fecha_prestamo=s[2], fecha_devolucion=s[3], aprobada=s[4]) for s in solicitudes]

    @staticmethod
    def obtener_por_cliente(id_cliente):
        """Obtiene todas las solicitudes de un cliente específico"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT * FROM Solicitudes WHERE id_cliente = %s", (id_cliente,))
        solicitudes = cursor.fetchall()
        conexion.cerrar()

        return [Solicitud(id_solicitud=s[0], id_cliente=s[1], fecha_prestamo=s[2], fecha_devolucion=s[3], aprobada=s[4]) for s in solicitudes]

    @staticmethod
    def agregar(id_cliente, fecha_prestamo, fecha_devolucion, aprobada=False):
        """Agrega una nueva solicitud"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        query = "INSERT INTO Solicitudes (id_cliente, fecha_prestamo, fecha_devolucion, aprobada) VALUES (%s, %s, %s, %s)"
        values = (id_cliente, fecha_prestamo, fecha_devolucion, aprobada)
        cursor.execute(query, values)
        conexion.connection.commit()
        conexion.cerrar()
