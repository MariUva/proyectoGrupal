from ConexionBD import ConexionDB


class Cliente:
    def __init__(self, id_cliente, nombre, email, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @staticmethod
    def obtener_todos():
        """Obtiene todos los clientes"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        conexion.cerrar()

        return [Cliente(id_cliente=c[0], nombre=c[1], email=c[2], telefono=c[3]) for c in clientes]

    @staticmethod
    def obtener_por_id(id_cliente):
        """Obtiene un cliente por ID"""
        conexion = ConexionDB()
        conexion.conectar()
        cursor = conexion.connection.cursor()

        cursor.execute("SELECT * FROM Clientes WHERE id_cliente = %s", (id_cliente,))
        cliente_data = cursor.fetchone()
        conexion.cerrar()

        if cliente_data:
            return Cliente(id_cliente=cliente_data[0], nombre=cliente_data[1], email=cliente_data[2], telefono=cliente_data[3])
        return None
