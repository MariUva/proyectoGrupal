# En Carro.py
class Carro:
    def __init__(self):
        self.objetos = []  # Lista para almacenar productos

    def agregar_producto(self, producto):
        self.objetos.append(producto)  # Método para agregar un producto al carro
