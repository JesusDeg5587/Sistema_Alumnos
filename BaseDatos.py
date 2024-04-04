import sqlite3
import tk


def conectar_base_de_datos():
    conn = sqlite3.connect('base_de_datos.db')
    c = conn.cursor()
    return conn, c

def crear_tabla_usuarios():
    conn, c = conectar_base_de_datos()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (nombre TEXT PRIMARY KEY NOT NULL, contraseña TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def crear_tabla_alumnos():
    conn, c = conectar_base_de_datos()
    c.execute('''CREATE TABLE IF NOT EXISTS alumnos
                 (nombre TEXT PRIMARY KEY NOT NULL, matricula TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def crear_tabla_tareas():
    conn, c = conectar_base_de_datos()
    c.execute('''CREATE TABLE IF NOT EXISTS tareas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def agregar_usuario(nombre, contraseña):
    conn, c = conectar_base_de_datos()
    c.execute("INSERT INTO usuarios (nombre, contraseña) VALUES (?, ?)", (nombre, contraseña))
    conn.commit()
    conn.close()

def agregar_alumno(nombre, matricula):
    conn, c = conectar_base_de_datos()
    c.execute("INSERT INTO alumnos (nombre, matricula) VALUES (?, ?)", (nombre, matricula))
    conn.commit()
    conn.close()

def agregar_tarea(nombre):
    conn, c = conectar_base_de_datos()
    c.execute("INSERT INTO tareas (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

def obtener_tareas():
    conn, c = conectar_base_de_datos()
    c.execute("SELECT nombre FROM tareas")
    tareas = [row[0] for row in c.fetchall()]
    conn.close()
    return tareas
def crear_tabla_archivos():
    conn, c = conectar_base_de_datos()
    c.execute('''CREATE TABLE IF NOT EXISTS archivos
                 (tarea TEXT NOT NULL, archivo TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def mostrar_archivos(tarea):
    ventana_archivos = tk.Toplevel(root)
    ventana_archivos.title(f"Archivos Subidos para la Tarea: {tarea}")
    center_window(ventana_archivos)

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


# Crear las tablas si no existen
crear_tabla_usuarios()
crear_tabla_alumnos()
crear_tabla_tareas()
crear_tabla_archivos()
