import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil
import sqlite3
from BaseDatos import agregar_usuario, agregar_alumno, agregar_tarea, obtener_tareas

def conectar_base_de_datos():
    conn = sqlite3.connect('base_de_datos.db')
    c = conn.cursor()
    return conn, c

def center_window(window):
    window.update_idletasks()
    width = 400
    height = 200
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def abrir_ventana_registro(tipo_usuario, root):
    def registrar_usuario():
        nombre = nombre_entry.get()
        contraseña = contraseña_entry.get()
        confirmar_contraseña = confirmar_contraseña_entry.get()
        if tipo_usuario == "alumno":
            matricula = matricula_entry.get()

        if contraseña == confirmar_contraseña:
            if tipo_usuario == "alumno" and len(matricula) != 10:
                messagebox.showerror("Error", "La matrícula debe tener 10 números.")
            else:
                agregar_usuario(nombre, contraseña)
                if tipo_usuario == "alumno":
                    agregar_alumno(nombre, matricula)
                messagebox.showinfo("Registro Exitoso", f"{tipo_usuario.capitalize()} registrado correctamente.")
                ventana_registro.destroy()
        else:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")

    ventana_registro = tk.Toplevel(root)
    ventana_registro.title(f"Registrar {tipo_usuario.capitalize()}")
    center_window(ventana_registro)

    nombre_label = tk.Label(ventana_registro, text="Nombre:")
    nombre_label.grid(row=0, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(ventana_registro)
    nombre_entry.grid(row=0, column=1, padx=10, pady=5)

    contraseña_label = tk.Label(ventana_registro, text="Contraseña:")
    contraseña_label.grid(row=1, column=0, padx=10, pady=5)
    contraseña_entry = tk.Entry(ventana_registro, show="*")
    contraseña_entry.grid(row=1, column=1, padx=10, pady=5)

    confirmar_contraseña_label = tk.Label(ventana_registro, text="Confirmar Contraseña:")
    confirmar_contraseña_label.grid(row=2, column=0, padx=10, pady=5)
    confirmar_contraseña_entry = tk.Entry(ventana_registro, show="*")
    confirmar_contraseña_entry.grid(row=2, column=1, padx=10, pady=5)

    if tipo_usuario == "alumno":
        matricula_label = tk.Label(ventana_registro, text="Matrícula:")
        matricula_label.grid(row=3, column=0, padx=10, pady=5)
        matricula_entry = tk.Entry(ventana_registro)
        matricula_entry.grid(row=3, column=1, padx=10, pady=5)

    registrar_button = tk.Button(ventana_registro, text="Registrar", command=registrar_usuario)
    registrar_button.grid(row=4, columnspan=2, padx=10, pady=5)

def abrir_ventana_gestion_escolar(usuario, root):
    def abrir_ventana_tarea():
        def subir_tarea():
            nombre_tarea = nombre_tarea_entry.get()
            agregar_tarea(nombre_tarea)
            messagebox.showinfo("Tarea Subida", f"La tarea '{nombre_tarea}' ha sido subida.")

        ventana_tarea = tk.Toplevel(root)
        ventana_tarea.title("Agregar Tarea")
        center_window(ventana_tarea)

        nombre_tarea_label = tk.Label(ventana_tarea, text="Nombre de la Tarea:")
        nombre_tarea_label.grid(row=0, column=0, padx=10, pady=5)
        nombre_tarea_entry = tk.Entry(ventana_tarea)
        nombre_tarea_entry.grid(row=0, column=1, padx=10, pady=5)

        subir_tarea_button = tk.Button(ventana_tarea, text="Subir Tarea", command=subir_tarea)
        subir_tarea_button.grid(row=1, columnspan=2, padx=10, pady=5)

    def ver_tareas_alumnos():
        ventana_ver_tareas_alumnos = tk.Toplevel(root)
        ventana_ver_tareas_alumnos.title("Tareas Subidas por Alumnos")
        center_window(ventana_ver_tareas_alumnos)

        tareas = obtener_tareas()
        if tareas:
            for tarea in tareas:
                tarea_label = tk.Label(ventana_ver_tareas_alumnos, text=f"Tarea: {tarea[0]}")
                tarea_label.pack(padx=10, pady=5)

                ver_archivos_button = tk.Button(ventana_ver_tareas_alumnos, text="Ver Archivos",
                                                command=lambda tarea=tarea[0]: mostrar_archivos(tarea))
                ver_archivos_button.pack(pady=5)
        else:
            sin_tareas_label = tk.Label(ventana_ver_tareas_alumnos, text="No hay tareas disponibles.")
            sin_tareas_label.pack(padx=10, pady=5)

    ventana_gestion_escolar = tk.Toplevel(root)
    ventana_gestion_escolar.title("Gestión Escolar")
    center_window(ventana_gestion_escolar)

    if usuario == "admin":
        btn_agregar_profesor = tk.Button(ventana_gestion_escolar, text="Agregar Profesor",
                                         command=lambda: abrir_ventana_registro("profesor", root))
        btn_agregar_profesor.pack(pady=5)

    btn_agregar_alumno = tk.Button(ventana_gestion_escolar, text="Agregar Alumno",
                                   command=lambda: abrir_ventana_registro("alumno", root))
    btn_agregar_alumno.pack(pady=5)

    if usuario == "profesor":
        btn_agregar_tarea = tk.Button(ventana_gestion_escolar, text="Agregar Tarea", command=abrir_ventana_tarea)
        btn_agregar_tarea.pack(pady=5)

        btn_ver_tareas_alumnos = tk.Button(ventana_gestion_escolar, text="Ver Tareas de Alumnos",
                                           command=ver_tareas_alumnos)
        btn_ver_tareas_alumnos.pack(pady=5)

def mostrar_archivos(tarea):
    ventana_archivos = tk.Toplevel(root)
    ventana_archivos.title(f"Archivos Subidos para la Tarea: {tarea}")
    center_window(ventana_archivos)

    # Obtener lista de archivos
    conn, c = conectar_base_de_datos()
    c.execute("SELECT archivo FROM archivos WHERE tarea = ?", (tarea,))
    archivos = c.fetchall()
    conn.close()

    if archivos:
        for archivo in archivos:
            archivo_label = tk.Label(ventana_archivos, text=archivo[0])
            archivo_label.pack(padx=10, pady=5)
    else:
        sin_archivos_label = tk.Label(ventana_archivos, text="No hay archivos subidos para esta tarea.")
        sin_archivos_label.pack(padx=10, pady=5)

def iniciar_sesion(tipo_usuario, root):
    def verificar_credenciales():
        username = username_entry.get()
        password = password_entry.get()

        if tipo_usuario == "admin" and username == "admin" and password == "admin":
            ventana_login.destroy()
            abrir_ventana_gestion_escolar(tipo_usuario, root)
        else:
            conn, c = conectar_base_de_datos()
            c.execute("SELECT contraseña FROM usuarios WHERE nombre = ?", (username,))
            result = c.fetchone()
            conn.close()

            if result and result[0] == password:
                messagebox.showinfo("Inicio de Sesión Exitoso", f"Bienvenido, {username}!")
                if tipo_usuario == "profesor":
                    ventana_login.destroy()
                    abrir_ventana_gestion_escolar(tipo_usuario, root)
                elif tipo_usuario == "alumno":
                    ventana_login.destroy()
                    mostrar_tareas_alumno(root)  # Mostrar las tareas después del mensaje de bienvenida
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

    ventana_login = tk.Toplevel(root)
    ventana_login.title(f"Iniciar Sesión como {tipo_usuario.capitalize()}")
    center_window(ventana_login)

    login_label = tk.Label(ventana_login, text=f"Iniciar Sesión como {tipo_usuario.capitalize()}")
    login_label.grid(row=0, columnspan=2, padx=10, pady=5)

    username_label = tk.Label(ventana_login, text="Usuario:")
    username_label.grid(row=1, column=0, padx=10, pady=5)
    username_entry = tk.Entry(ventana_login)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = tk.Label(ventana_login, text="Contraseña:")
    password_label.grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(ventana_login, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    login_button = tk.Button(ventana_login, text="Iniciar Sesión", command=verificar_credenciales)
    login_button.grid(row=3, columnspan=2, padx=10, pady=5)

# Función para subir tarea
def subir_tarea(tarea):
    archivo = filedialog.askopenfilename(initialdir="/", title="Seleccionar Archivo")
    if archivo:
        # Copiar el archivo a una ubicación específica
        nombre_archivo = os.path.basename(archivo)
        destino = f"archivos_tareas/{tarea}/{nombre_archivo}"  # Carpeta por tarea
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy(archivo, destino)

        # Insertar la información del archivo en la base de datos
        conn, c = conectar_base_de_datos()
        c.execute("INSERT INTO archivos (tarea, archivo) VALUES (?, ?)", (tarea, nombre_archivo))
        conn.commit()
        conn.close()

        messagebox.showinfo("Subir Tarea", "Tarea subida exitosamente.")


# En la función mostrar_tareas_alumno(), para cada tarea, agregar un botón "Subir Tarea" y un botón "Ver Archivos"
def mostrar_tareas_alumno(root):
    ventana_tareas_alumno = tk.Toplevel(root)
    ventana_tareas_alumno.title("Tareas Disponibles para Alumnos")
    center_window(ventana_tareas_alumno)

    tareas = obtener_tareas()
    if tareas:
        for i, tarea in enumerate(tareas):
            tarea_label = tk.Label(ventana_tareas_alumno, text=f"Tarea {i+1}: {tarea[0]}")
            tarea_label.pack(padx=10, pady=5)

            subir_tarea_button = tk.Button(ventana_tareas_alumno, text="Subir Tarea",
                                           command=lambda tarea=tarea[0]: subir_tarea(tarea))
            subir_tarea_button.pack(pady=5)

            ver_archivos_button = tk.Button(ventana_tareas_alumno, text="Ver Archivos",
                                             command=lambda tarea=tarea[0]: mostrar_archivos(tarea))
            ver_archivos_button.pack(pady=5)
    else:
        sin_tareas_label = tk.Label(ventana_tareas_alumno, text="No hay tareas disponibles.")
        sin_tareas_label.pack(padx=10, pady=5)

root = tk.Tk()
root.title("Seleccion de Usuario")
center_window(root)

login_admin_button = tk.Button(root, text="Iniciar Sesión como Admin", command=lambda: iniciar_sesion("admin", root))
login_admin_button.pack(pady=10)

login_profesor_button = tk.Button(root, text="Iniciar Sesión como Profesor", command=lambda: iniciar_sesion("profesor", root))
login_profesor_button.pack(pady=10)

login_alumno_button = tk.Button(root, text="Iniciar Sesión como Alumno", command=lambda: iniciar_sesion("alumno", root))
login_alumno_button.pack(pady=10)

root.mainloop()
