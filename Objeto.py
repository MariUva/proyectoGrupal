class Objeto:
    def __init__(self, id_objeto, nombre, descripcion, estado):
        self.id_objeto = id_objeto
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

    @staticmethod
    def obtener_todos():
        """Obtiene todos los objetos"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT * FROM Objetos WHERE estado = 'disponible'")
        objetos = cursor.fetchall()
        conexion.cerrar()

        return [Objeto(id_objeto=o[0], nombre=o[1], descripcion=o[2], estado=o[3]) for o in objetos]

    @staticmethod
    def obtener_reservados():
        """Obtiene todos los objetos reservados"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT * FROM Objetos WHERE estado = 'prestado'")
        objetos = cursor.fetchall()
        conexion.cerrar()

        return [Objeto(id_objeto=o[0], nombre=o[1], descripcion=o[2], estado=o[3]) for o in objetos]
