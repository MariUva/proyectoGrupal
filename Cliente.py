class Cliente:
    def __init__(self, id_cliente, nombre, email, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f"Cliente({self.nombre}, {self.email})"
