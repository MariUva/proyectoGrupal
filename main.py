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
        """Actualiza la lista de objetos disponibles y prestados."""
        self.lista_objetos.delete(0, tk.END)
        self.lista_reservados.delete(0, tk.END)

        # Se actualizan las listas disponibles y prestados en función del estado de cada producto
        for objeto in self.objetos:
            if objeto.estado == "disponible":
                self.lista_objetos.insert(tk.END, f"{objeto.nombre} - {objeto.descripcion}")
            elif objeto.estado == "prestado":
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
        if producto.estado == "prestado":
            messagebox.showwarning("Advertencia", "Este producto ya está prestado.")
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
        """Muestra el formulario para ingresar el ID del cliente y validar si está registrado."""
        formulario_ventana = tk.Toplevel(self.root)
        formulario_ventana.title("Validar ID Cliente")
        formulario_ventana.geometry("400x300")

        tk.Label(formulario_ventana, text="ID Cliente:").pack(pady=10)
        id_cliente_entry = tk.Entry(formulario_ventana, width=40)
        id_cliente_entry.pack(pady=10)

        # Botón para validar el ID
        tk.Button(formulario_ventana, text="Validar ID", command=lambda: self.validar_id_cliente(id_cliente_entry.get(), formulario_ventana)).pack(pady=10)

    def validar_id_cliente(self, id_cliente, formulario_ventana):
        """Valida el ID del cliente y muestra los datos si el ID es correcto."""
        if not id_cliente:
            messagebox.showwarning("Advertencia", "Por favor ingrese el ID del cliente.")
            return

        # Conectar a la base de datos y verificar si el ID del cliente existe
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, email, telefono FROM Clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        conn.close()

        if cliente:
            # El cliente está registrado, proceder con la segunda fase
            self.mostrar_datos_cliente(cliente, formulario_ventana)
        else:
            # El ID no está registrado
            messagebox.showwarning("Error", "Lo sentimos, no está registrado en el sistema.")
            formulario_ventana.destroy()

    def mostrar_datos_cliente(self, cliente, formulario_ventana):
        """Muestra los datos del cliente y permite elegir las fechas de préstamo."""
        formulario_ventana.destroy()

        # Crear ventana para mostrar los datos del cliente y las fechas
        datos_ventana = tk.Toplevel(self.root)
        datos_ventana.title("Datos del Cliente y Fechas de Préstamo")
        datos_ventana.geometry("400x400")

        # Mostrar los datos del cliente
        tk.Label(datos_ventana, text="Nombre: " + cliente[1]).pack(pady=5)
        tk.Label(datos_ventana, text="Email: " + cliente[2]).pack(pady=5)
        tk.Label(datos_ventana, text="Teléfono: " + cliente[3]).pack(pady=5)

        # Selección de fechas
        tk.Label(datos_ventana, text="Fecha de Solicitud:").pack(pady=10)
        fecha_solicitud = DateEntry(datos_ventana, width=12, background="darkblue", foreground="white", borderwidth=2)
        fecha_solicitud.pack(pady=5)

        tk.Label(datos_ventana, text="Fecha de Devolución:").pack(pady=10)
        fecha_devolucion = DateEntry(datos_ventana, width=12, background="darkblue", foreground="white", borderwidth=2)
        fecha_devolucion.pack(pady=5)

        # Botón para realizar la solicitud
        tk.Button(datos_ventana, text="Realizar Solicitud", font=("Arial", 12), command=lambda: self.realizar_solicitud(cliente[0], fecha_solicitud.get_date(), fecha_devolucion.get_date(), datos_ventana)).pack(pady=10)

    def realizar_solicitud(self, id_cliente, fecha_solicitud, fecha_devolucion, formulario_ventana):
        """Realiza la solicitud de préstamo con los datos ingresados."""
        if not id_cliente:
            messagebox.showwarning("Advertencia", "Debe ingresar un ID de cliente válido.")
            return

        # Crear una nueva solicitud y asociar los objetos seleccionados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Insertar datos en la tabla Solicitudes (solo con id_cliente y fechas)
        cursor.execute("""
            INSERT INTO Solicitudes (id_cliente, fecha_prestamo, fecha_devolucion)
            VALUES (%s, %s, %s)
        """, (id_cliente, fecha_solicitud, fecha_devolucion))
        solicitud_id = cursor.lastrowid

        # Insertar los productos prestados
        for producto in self.carro.objetos:
            cursor.execute("UPDATE Objetos SET estado='prestado' WHERE id_objeto=%s", (producto.id_objeto,))  # Cambiar id por id_objeto
            cursor.execute("INSERT INTO DetalleSolicitud (id_solicitud, id_objeto) VALUES (%s, %s)", (solicitud_id, producto.id_objeto))  # Cambiar id por id_objeto

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


# Crear la ventana principal de la aplicación
root = tk.Tk()
app = QMDApp(root)
root.mainloop()
