import tkinter as tk
from tkinter import messagebox

from Carro import Carro
from Cliente import Cliente
from Objeto import Objeto
import GestorDePrestamos  # Se importa el módulo

class QMDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema QMD - Gestión de Préstamos")
        self.root.geometry("800x500")
        self.centrar_ventana(800, 550)

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

        #Productos disponibles
        tk.Label(frame_productos, text="Productos Disponibles", font=("Arial", 14, "bold"), fg="green").grid(row=0, column=0, padx=10, sticky="n", columnspan=1)
        self.lista_objetos = tk.Listbox(frame_productos, width=50, height=8)
        self.lista_objetos.grid(row=1, column=0, padx=10)

        # Productos reservados
        tk.Label(frame_productos, text="Productos Reservados", font=("Arial", 14, "bold"), fg="red").grid(row=0, column=1, padx=10, sticky="n", columnspan=1)
        self.lista_reservados = tk.Listbox(frame_productos, width=50, height=8)
        self.lista_reservados.grid(row=1, column=1, padx=10)

        # Se asegura de que ambas secciones estén centradas, usando el método grid
        frame_productos.grid_columnconfigure(0, weight=1)
        frame_productos.grid_columnconfigure(1, weight=1)

        # Botón para agregar el producto al carro (verde)
        tk.Button(self.root, text="Agregar al Carro", font=("Arial", 12), command=self.agregar_producto_carro, bg="green", fg="white").pack(pady=10)

        # Botón para eliminar producto del carro (rojo)
        tk.Button(self.root, text="Eliminar Producto del Carro", font=("Arial", 12), command=self.eliminar_producto_carro, bg="red", fg="white").pack(pady=10)

        # Carro de objetos
        tk.Label(self.root, text="Carro de Objetos:", font=("Arial", 14, "bold")).pack()
        self.lista_carro = tk.Listbox(self.root, width=60, height=5)
        self.lista_carro.pack(pady=5)

        # Botón para realizar la solicitud (azul)
        tk.Button(self.root, text="Realizar Solicitud", font=("Arial", 12), command=self.mostrar_formulario_solicitud, bg="blue", fg="white").pack(pady=10)

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

    def agregar_producto_carro(self):
        """Agrega un producto al carro."""
        seleccion = self.lista_objetos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para agregar al carro.")
            return

        # Agregar el producto al carro
        index = seleccion[0]
        producto = self.objetos[index]
        if producto.estado == "reservado":
            messagebox.showwarning("Advertencia", "Este producto ya está reservado.")
            return

        # Agregar el producto al carro y actualizar el estado
        self.carro.agregar_producto(producto)
        self.lista_carro.insert(tk.END, f"{producto.nombre} - {producto.descripcion}")

        # También actualizar la lista de objetos disponibles
        self.actualizar_lista_objetos()

    def eliminar_producto_carro(self):
        """Elimina un producto del carro."""
        seleccion = self.lista_carro.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")
            return

        # Eliminar el producto de la lista del carro
        index = seleccion[0]
        producto = self.carro.objetos[index]
        self.carro.objetos.remove(producto)
        self.lista_carro.delete(index)

        # Actualizar el estado del producto a "disponible" y volver a agregarlo a los objetos disponibles
        producto.estado = "disponible"
        self.actualizar_lista_objetos()

    def mostrar_formulario_solicitud(self):
        """Muestra un formulario para ingresar los datos del cliente."""
        # Crear una nueva ventana para la solicitud
        formulario_ventana = tk.Toplevel(self.root)
        formulario_ventana.title("Formulario de Solicitud")
        formulario_ventana.geometry("400x300")

        # Labels y campos de entrada
        tk.Label(formulario_ventana, text="Nombre:").pack(pady=5)
        nombre_entry = tk.Entry(formulario_ventana, width=40)
        nombre_entry.pack(pady=5)

        tk.Label(formulario_ventana, text="Email:").pack(pady=5)
        email_entry = tk.Entry(formulario_ventana, width=40)
        email_entry.pack(pady=5)

        tk.Label(formulario_ventana, text="Teléfono:").pack(pady=5)
        telefono_entry = tk.Entry(formulario_ventana, width=40)
        telefono_entry.pack(pady=5)

        # Función para enviar la solicitud
        def enviar_solicitud():
            nombre = nombre_entry.get()
            email = email_entry.get()
            telefono = telefono_entry.get()

            # Validación de los datos
            if not nombre or not email or not telefono:
                messagebox.showerror("Error", "Debe completar todos los datos del cliente.")
                return

            # Crear cliente y solicitud
            cliente = Cliente(len(self.gestor.solicitudes) + 1, nombre, email, telefono)
            solicitud = self.gestor.crear_solicitud(cliente, self.carro.objetos)
            messagebox.showinfo("Solicitud realizada", f"Solicitud realizada con éxito.\nID: {solicitud['id']}")

            # Mover los productos del carro a "reservado"
            for producto in self.carro.objetos:
                producto.estado = "reservado"

            # Actualizar las listas
            self.actualizar_lista_objetos()

            # Limpiar el carro después de la solicitud
            self.carro.objetos.clear()
            self.lista_carro.delete(0, tk.END)

            formulario_ventana.destroy()  # Cerrar el formulario

        # Botón para enviar la solicitud
        tk.Button(formulario_ventana, text="Enviar Solicitud", command=enviar_solicitud).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = QMDApp(root)
    root.mainloop()
