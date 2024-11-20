import tkinter as tk
from tkinter import messagebox, simpledialog

from Carro import Carro
from Cliente import Cliente
from Objeto import Objeto
import GestorDePrestamos

import tkinter as tk
from tkinter import messagebox, simpledialog

from Carro import Carro
from Cliente import Cliente
from Objeto import Objeto
import GestorDePrestamos  # Se importa el módulo

class QMDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema QMD - Gestión de Préstamos")
        self.root.geometry("800x500")
        self.centrar_ventana(800, 500)

        # Crear instancias
        self.objetos = [
            Objeto(1, "Laptop", "Laptop HP de 14 pulgadas"),
            Objeto(2, "Proyector", "Proyector Epson 3D"),
            Objeto(3, "Tablet", "Tablet Samsung Galaxy Tab"),
        ]
        self.carro = Carro()
        self.gestor = GestorDePrestamos.GestorDePrestamos()  # Accede a la clase correctamente

        # Crear interfaz
        self.crear_interfaz()


    def centrar_ventana(self, ancho, alto):
        """Centra la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (ancho / 2))
        y_cordinate = int((screen_height / 2) - (alto / 2))
        self.root.geometry(f"{ancho}x{alto}+{x_cordinate}+{y_cordinate}")

    def crear_interfaz(self):
        # Título
        tk.Label(self.root, text="Sistema QMD - Gestión de Préstamos", font=("Arial", 20, "bold"), fg="darkblue").pack(pady=10)

        # Secciones de productos
        frame_productos = tk.Frame(self.root)
        frame_productos.pack(pady=10, fill="x", padx=20)

        # Productos disponibles
        tk.Label(frame_productos, text="Productos Disponibles", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, sticky="w")
        self.lista_objetos = tk.Listbox(frame_productos, width=40, height=15)
        self.lista_objetos.grid(row=1, column=0, padx=10)

        # Productos reservados
        tk.Label(frame_productos, text="Productos Reservados", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, sticky="w")
        self.lista_reservados = tk.Listbox(frame_productos, width=40, height=15)
        self.lista_reservados.grid(row=1, column=1, padx=10)

        # Botón agregar al carro
        tk.Button(self.root, text="Agregar al Carro", font=("Arial", 12), command=self.agregar_al_carro).pack(pady=10)

        # Carro de objetos
        tk.Label(self.root, text="Carro de Objetos:", font=("Arial", 14, "bold")).pack()
        self.lista_carro = tk.Listbox(self.root, width=60, height=5)
        self.lista_carro.pack(pady=5)

        # Botón realizar solicitud
        tk.Button(self.root, text="Realizar Solicitud", font=("Arial", 12), command=self.realizar_solicitud).pack(pady=10)

        # Ahora que todo está inicializado, podemos actualizar las listas
        self.actualizar_lista_objetos()

    def actualizar_lista_objetos(self):
        """Actualiza la lista de objetos disponibles y reservados."""
        self.lista_objetos.delete(0, tk.END)
        self.lista_reservados.delete(0, tk.END)

        for objeto in self.objetos:
            if objeto.estado == "disponible":
                self.lista_objetos.insert(tk.END, f"{objeto.nombre} - {objeto.descripcion}")
            elif objeto.estado == "reservado":
                self.lista_reservados.insert(tk.END, f"{objeto.nombre} - {objeto.descripcion}")

    def agregar_al_carro(self):
        """Agrega un objeto al carro."""
        seleccion = self.lista_objetos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un objeto.")
            return

        index = seleccion[0]
        objeto = self.objetos[index]
        self.carro.agregar_objeto(objeto)
        self.lista_carro.insert(tk.END, f"{objeto.nombre} - {objeto.descripcion}")
        self.actualizar_lista_objetos()

    def realizar_solicitud(self):
        """Realiza una solicitud de préstamo."""
        if not self.carro.objetos:
            messagebox.showwarning("Advertencia", "El carro está vacío.")
            return

        nombre = simpledialog.askstring("Cliente", "Ingrese su nombre:")
        email = simpledialog.askstring("Cliente", "Ingrese su email:")
        telefono = simpledialog.askstring("Cliente", "Ingrese su teléfono:")

        if not nombre or not email or not telefono:
            messagebox.showerror("Error", "Debe completar todos los datos del cliente.")
            return

        cliente = Cliente(len(self.gestor.solicitudes) + 1, nombre, email, telefono)
        solicitud = self.gestor.crear_solicitud(cliente, self.carro.objetos)
        messagebox.showinfo("Solicitud realizada", f"Solicitud realizada con éxito.\nID: {solicitud['id']}")
        self.carro.objetos.clear()
        self.lista_carro.delete(0, tk.END)
        self.actualizar_lista_objetos()


if __name__ == "__main__":
    root = tk.Tk()
    app = QMDApp(root)
    root.mainloop()
