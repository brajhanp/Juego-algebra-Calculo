import tkinter as tk
from tkinter import simpledialog
import sqlite3
import random

# Variables globales para el juego
indice_pregunta = 0
puntaje = 0
preguntas = []

# Configuración inicial de la base de datos
def crear_base_datos():
    conexion = sqlite3.connect("trivia.db")
    cursor = conexion.cursor()

    # Crear tabla de preguntas (si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            opcion1 TEXT NOT NULL,
            opcion2 TEXT NOT NULL,
            opcion3 TEXT NOT NULL,
            opcion4 TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    # Crear tabla de records (si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puntaje INTEGER NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Llamada inicial para crear la base de datos si no existe
crear_base_datos()

# Función para agregar preguntas de ejemplo a la base de datos
def agregar_preguntas_ejemplo(categoria):
    preguntas_ejemplo = {
        "Calculo": [
            ("¿Cuál es la derivada de 76x^2 - 56x + 45?", "345x - 56", "150x - 56", "200x - 65", "152x - 56", "152x - 56"),
            ("¿Cuál es la derivada de x^2?", "2x", "x^2", "1", "x", "2x"),
            ("¿Cuál es la integral de x?", "x^2/2", "x", "ln(x)", "1", "x^2/2"),
            ("¿Cuál es la derivada de sen(x)?", "cos(x)", "sen(x)", "-cos(x)", "-sen(x)", "cos(x)"),
            ("¿Cuál es la integral de cos(x)?", "sen(x) + C", "-sen(x) + C", "cos(x) + C", "x + C", "sen(x) + C"),
            ("¿Cuál es la derivada de e^x?", "e^x", "x^e", "ln(x)", "x^2", "e^x"),
            ("¿Qué representa el valor de una derivada en un punto?", "El área bajo la curva", "La pendiente de la recta tangente", "El valor máximo de la función", "El valor mínimo de la función", "La pendiente de la recta tangente"),
            ("¿Cuál es la segunda derivada de x^3?", "6x", "3x^2", "2x", "x^3", "6x"),
            ("¿Cuál es la derivada de ln(x)?", "1/x", "x", "ln(x)/x", "1/(ln(x))", "1/x"),
            ("¿Qué significa que una función sea continua en un punto?", 
             "Que existe su derivada en ese punto", 
             "Que no tiene saltos ni discontinuidades en ese punto", 
             "Que tiene un máximo o un mínimo", 
             "Que la función siempre crece en ese punto", 
             "Que no tiene saltos ni discontinuidades en ese punto")
        ],
        "Algebra": [
            ("¿Cuál es la solución de 2x + 3 = 7?", "x = 2", "x = 4", "x = -2", "x = 1", "x = 2"),
            ("¿Cuál es el valor de x en 3x - 5 = 10?", "x = 5", "x = 3", "x = 4", "x = 6", "x = 5"),
            ("¿Cómo se sabe cuándo es máximo?", 
             "es máximo cuando es mayor a cero", 
             "es máximo cuando es menor a cero", 
             "es máximo cuando es igual a cero", 
             "cuando es divisible entre 2", 
             "es máximo cuando es menor a cero"),
            ("¿Qué propiedad cumple la suma de dos números opuestos?", 
             "Es igual a cero", 
             "Es igual al producto de los números", 
             "Es igual a uno", 
             "Es un número negativo", 
             "Es igual a cero"),
            ("¿Cómo se simplifica (x^2 * x^3)?", 
             "x^5", 
             "x^6", 
             "x^2", 
             "x^9", 
             "x^5"),
            ("Si 5x - 3 = 7, ¿cuánto vale x?", 
             "x = 2", 
             "x = 5", 
             "x = 1", 
             "x = -2", 
             "x = 2"),
            ("¿Cuál es el resultado de (a + b)^2?", 
             "a^2 + 2ab + b^2", 
             "a^2 - b^2", 
             "a^2 + b^2", 
             "2a + b", 
             "a^2 + 2ab + b^2"),
            ("¿Qué indica el discriminante de una ecuación cuadrática?", 
             "El número de soluciones reales", 
             "El valor máximo de la función", 
             "La pendiente de la recta tangente", 
             "El área bajo la curva", 
             "El número de soluciones reales"),
            ("¿Qué es una identidad algebraica?", 
             "Una igualdad que se cumple para todos los valores de las variables", 
             "Una ecuación que no tiene solución", 
             "Una operación con polinomios", 
             "Un método para resolver ecuaciones", 
             "Una igualdad que se cumple para todos los valores de las variables"),
            ("¿Qué valor hace que x^2 - 4 = 0 sea verdadera?", 
             "x = ±2", 
             "x = 4", 
             "x = 2", 
             "x = 0", 
             "x = ±2")
        ]
    }

    # Agregar preguntas de ejemplo para la categoría
    for pregunta, op1, op2, op3, op4, respuesta in preguntas_ejemplo.get(categoria, []):
        conexion = sqlite3.connect("trivia.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO preguntas (pregunta, opcion1, opcion2, opcion3, opcion4, respuesta_correcta, categoria) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (pregunta, op1, op2, op3, op4, respuesta, categoria))
        conexion.commit()
        conexion.close()

# Verificar si la categoría ya tiene preguntas, si no agregar preguntas de ejemplo
def verificar_categoria(categoria):
    conexion = sqlite3.connect("trivia.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM preguntas WHERE categoria = ?", (categoria,))
    count = cursor.fetchone()[0]
    if count == 0:
        agregar_preguntas_ejemplo(categoria)
    conexion.close()

# Cargar preguntas de la base de datos
def cargar_preguntas(categoria):
    global preguntas
    conexion = sqlite3.connect("trivia.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT pregunta, opcion1, opcion2, opcion3, opcion4, respuesta_correcta FROM preguntas WHERE categoria = ?", (categoria,))
    preguntas = cursor.fetchall()
    conexion.close()
    random.shuffle(preguntas)  # Mezclar las preguntas

# Guardar récord en la base de datos
def guardar_record(nombre, puntaje):
    conexion = sqlite3.connect("trivia.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO records (nombre, puntaje) VALUES (?, ?)", (nombre, puntaje))
    conexion.commit()
    conexion.close()

# Mostrar la tabla de récords en una ventana emergente
def mostrar_records():
    conexion = sqlite3.connect("trivia.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, puntaje FROM records ORDER BY puntaje DESC LIMIT 10")
    records = cursor.fetchall()
    conexion.close()
    
    # Crear ventana emergente para mostrar los récords
    records_window = tk.Toplevel(ventana)
    records_window.title("Récords")
    
    tk.Label(records_window, text="Top 10 Récords", font=("Arial", 14)).pack(pady=10)
    for i, (nombre, puntaje) in enumerate(records, start=1):
        tk.Label(records_window, text=f"{i}. {nombre}: {puntaje} puntos", font=("Arial", 12)).pack()

# Verificar respuesta del usuario
def verificar_respuesta(respuesta):
    global indice_pregunta, puntaje
    if respuesta == preguntas[indice_pregunta][5]:  # La respuesta correcta es el último elemento en cada tupla
        puntaje += 1
        resultado_label.config(text="¡Correcto!", fg="green")
    else:
        resultado_label.config(text=f"Incorrecto. La respuesta correcta era: {preguntas[indice_pregunta][5]}", fg="red")
    
    indice_pregunta += 1
    actualizar_pregunta()

# Actualizar la pregunta y opciones
def actualizar_pregunta():
    if indice_pregunta < len(preguntas):
        pregunta = preguntas[indice_pregunta]
        pregunta_label.config(text=pregunta[0])
        for i, opcion in enumerate(pregunta[1:5]):
            botones_opciones[i].config(text=opcion, command=lambda op=opcion: verificar_respuesta(op))
        puntaje_label.config(text=f"Puntaje: {puntaje}")
    else:
        finalizar_juego()

# Finalizar el juego y guardar puntaje
def finalizar_juego():
    global puntaje
    pregunta_label.config(text="¡Juego terminado!")
    for boton in botones_opciones:
        boton.config(state="disabled")
    resultado_label.config(text=f"Puntaje final: {puntaje}/{len(preguntas)}")

    # Pedir nombre del jugador y guardar puntaje
    nombre = simpledialog.askstring("Guardar puntaje", "Ingresa tu nombre:")
    if nombre:
        guardar_record(nombre, puntaje)
        resultado_label.config(text=f"¡Puntaje guardado! Gracias por jugar, {nombre}.")

# Función para iniciar el juego
def iniciar_juego(categoria):
    menu_inicio_frame.pack_forget()  # Ocultar el menú de inicio
    verificar_categoria(categoria)  # Verificar si ya existen preguntas para la categoría
    cargar_preguntas(categoria)
    trivia_frame.pack(fill="both", expand=True)  # Mostrar el frame del juego
    actualizar_pregunta()

# Función para seleccionar la categoría
def seleccionar_categoria(categoria):
    iniciar_juego(categoria)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Juego de Trivia")
ventana.geometry("500x400")

# Frame del menú de inicio
menu_inicio_frame = tk.Frame(ventana)
menu_inicio_frame.pack(fill="both", expand=True)

# Fondo del menú de inicio (usando un .gif o .png compatible)
fondo_menu_tk = tk.PhotoImage(file="Fondo.png")  # Asegúrate de tener la imagen en el formato adecuado

# Canvas para el fondo del menú
canvas_menu = tk.Canvas(menu_inicio_frame, width=500, height=400)
canvas_menu.pack(fill="both", expand=True)
canvas_menu.create_image(0, 0, image=fondo_menu_tk, anchor="nw")

# Botones para elegir categoría
calculo_button = tk.Button(menu_inicio_frame, text="Cálculo", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", command=lambda: seleccionar_categoria("Calculo"))
algebra_button = tk.Button(menu_inicio_frame, text="Álgebra", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", command=lambda: seleccionar_categoria("Algebra"))
canvas_menu.create_window(250, 150, window=calculo_button)
canvas_menu.create_window(250, 200, window=algebra_button)

# Frame para el juego de trivia
trivia_frame = tk.Frame(ventana)

# Cargar imagen de fondo del juego (usando un .gif o .png compatible)
fondo_trivia_tk = tk.PhotoImage(file="Fondo.png")  # Asegúrate de tener la imagen en el formato adecuado

# Canvas para el fondo del juego
canvas_trivia = tk.Canvas(trivia_frame, width=500, height=400)
canvas_trivia.pack(fill="both", expand=True)
canvas_trivia.create_image(0, 0, image=fondo_trivia_tk, anchor="nw")

# Widgets del juego en el frame del juego
pregunta_label = tk.Label(trivia_frame, text="", font=("Arial", 14), bg="#f0f0f0", wraplength=400)
canvas_trivia.create_window(250, 50, window=pregunta_label)

# Modificación de los botones para que sean más largos
botones_opciones = []
for i in range(4):
    boton = tk.Button(trivia_frame, text="", font=("Arial", 12), width=25)  # Aumenté el width para que los botones sean más largos
    botones_opciones.append(boton)
    canvas_trivia.create_window(250, 120 + i * 50, window=boton)

resultado_label = tk.Label(trivia_frame, text="", font=("Arial", 12), bg="#f0f0f0")
canvas_trivia.create_window(250, 330, window=resultado_label)

puntaje_label = tk.Label(trivia_frame, text=f"Puntaje: {puntaje}", font=("Arial", 12), bg="#f0f0f0")
canvas_trivia.create_window(250, 360, window=puntaje_label)

# Iniciar el programa con el menú de inicio
ventana.mainloop()
