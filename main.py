import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from Carro import Carro
from Cliente import Cliente
from Objeto import Objeto
import GestorDePrestamos
import mysql.connector

# Conexion con la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="root",  
        database="qmd"
    )

class QMDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema QMD - Gestión de Préstamos")
        self.root.geometry("800x500")
        self.centrar_ventana(800, 550)

        # Crear instancias de objetos
        self.objetos = []
        self.carro = Carro()
        self.gestor = GestorDePrestamos.GestorDePrestamos()

        # Cargar los objetos disponibles de la base de datos
        self.cargar_objetos_bd()

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
        tk.Label(frame_productos, text="Productos Disponibles", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, sticky="n", columnspan=1)
        self.lista_objetos = tk.Listbox(frame_productos, width=50, height=8)
        self.lista_objetos.grid(row=1, column=0, padx=10)

        # Productos reservados
        tk.Label(frame_productos, text="Productos Reservados", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, sticky="n", columnspan=1)
        self.lista_reservados = tk.Listbox(frame_productos, width=50, height=8)
        self.lista_reservados.grid(row=1, column=1, padx=10)

        # Se asegura de que ambas secciones estén centradas
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

        # Actualizar las listas de objetos
        self.actualizar_lista_objetos()

    def cargar_objetos_bd(self):
        """Carga los objetos disponibles desde la base de datos MySQL"""
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT id_objeto, nombre, descripcion, estado FROM Objetos")
        objetos_bd = cursor.fetchall()
        conn.close()

        for objeto in objetos_bd:
            objeto_id, nombre, descripcion, estado = objeto
            self.objetos.append(Objeto(objeto_id, nombre, descripcion, estado))

    def actualizar_lista_objetos(self):
        """Actualiza la lista de objetos disponibles y reservados."""
        self.lista_objetos.delete(0, tk.END)
        self.lista_reservados.delete(0, tk.END)

        # Se actualizan las listas disponibles y reservados en función del estado de cada producto
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

        # Agregar el producto al carro (sin cambiar su estado)
        self.carro.agregar_producto(producto)
        self.lista_carro.insert(tk.END, f"{producto.nombre} - {producto.descripcion}")

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
        """Muestra un formulario para ingresar los datos del cliente y fechas de préstamo."""
        formulario_ventana = tk.Toplevel(self.root)
        formulario_ventana.title("Formulario de Solicitud")
        formulario_ventana.geometry("400x400")

        tk.Label(formulario_ventana, text="Nombre:").pack(pady=5)
        nombre_entry = tk.Entry(formulario_ventana, width=40)
        nombre_entry.pack(pady=5)

        tk.Label(formulario_ventana, text="Email:").pack(pady=5)
        email_entry = tk.Entry(formulario_ventana, width=40)
        email_entry.pack(pady=5)

        tk.Label(formulario_ventana, text="Telefono:").pack(pady=5)
        telefono_entry = tk.Entry(formulario_ventana, width=40)
        telefono_entry.pack(pady=5)

        # Crear un calendario para la fecha de solicitud
        tk.Label(formulario_ventana, text="Fecha de Solicitud de Préstamo:").pack(pady=5)
        date_entry_fecha_emision = DateEntry(formulario_ventana, date_pattern='yyyy-mm-dd', width=20)
        date_entry_fecha_emision.pack(pady=5)

        tk.Label(formulario_ventana, text="Fecha de Devolución:").pack(pady=5)
        date_entry_fecha_expiracion = DateEntry(formulario_ventana, date_pattern='yyyy-mm-dd', width=20)
        date_entry_fecha_expiracion.pack(pady=5)

        tk.Button(formulario_ventana, text="Enviar Solicitud", command=lambda: self.realizar_solicitud(
            nombre_entry.get(), email_entry.get(), telefono_entry.get(), date_entry_fecha_emision.get(), date_entry_fecha_expiracion.get(), formulario_ventana
        )).pack(pady=10)

    def realizar_solicitud(self, nombre, email, telefono, fecha_solicitud, fecha_devolucion, formulario_ventana):
        """Realiza la solicitud de préstamo con los datos ingresados."""
        if not nombre or not email or not telefono:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Crear una nueva solicitud y asociar los objetos seleccionados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insertar datos en la tabla Solicitudes
        cursor.execute("INSERT INTO Solicitudes (nombre_cliente, email_cliente, telefono_cliente, fecha_solicitud, fecha_devolucion) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, email, telefono, fecha_solicitud, fecha_devolucion))
        solicitud_id = cursor.lastrowid

        # Insertar los productos reservados
        for producto in self.carro.objetos:
            cursor.execute("UPDATE Objetos SET estado='reservado' WHERE id_objeto=%s", (producto.id,))
            cursor.execute("INSERT INTO DetalleSolicitud (id_solicitud, id_objeto) VALUES (%s, %s)", (solicitud_id, producto.id))

        conn.commit()
        conn.close()

        # Cerrar la ventana del formulario
        formulario_ventana.destroy()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Solicitud realizada con éxito.")

        # Limpiar el carro y actualizar las listas de objetos
        self.carro.objetos.clear()
        self.lista_carro.delete(0, tk.END)
        self.actualizar_lista_objetos()

if __name__ == "__main__":
    root = tk.Tk()
    app = QMDApp(root)
    root.mainloop()
