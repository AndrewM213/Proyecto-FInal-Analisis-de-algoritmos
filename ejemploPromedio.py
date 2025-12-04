import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import random


estudiantes = []
Carreras = ["Ingeniería de Sistemas", "Ingenuería Civil", "Ingeniería de Software","Administración de Empresas", "Contabilidad", 
           "Marketing", "Derecho", "Medicina", "Arquitectura", "Psicología"]

def generar_datos_random(start_id=101):
    nombres_base = ["Ana Torres", "Carlos Ruiz", "Elena Gomez", "David Gil", "Beatriz Lima",
        "Fernando Solis", "Gloria Mendez", "Anthony Chavez", "Luisa Connor", "Miguel Silva",
        "Sofia Diaz", "Ben Soto", "Juan Perez", "Maria Rodriguez", "Jose Garcia",
        "Laura Martinez", "Miguel Hernandez", "Sofia Lopez", "Jorge Gonzalez", "Lucia Perez",
        "Antonio Sanchez", "Paula Rivera", "Francisco Torres", "Andrea Ramirez", "Manuel Flores",
        "Daniela Diaz", "Pedro Vasquez", "Carmen Castillo", "Alejandro Morales", "Veronica Reyes",
        "Roberto Gomez", "Florinda Meza", "Ruben Aguirre", "Ramon Valdes", "Maria Medina",
        "Luis Ulloa", "Cristia Jibaja", "Eduardo Molina", "Rodrigo Felix", "Sergio Ramos",
        "Diana Prince", "Gerald Mendez", "Steven Dominguez", "Natasha Benites", "Wanda Maximoff",
        "Walter Pariona", "Jesse Pinkman", "Andrew Morales", "Wilfredo Chiara", "Cecilia Rojas"]

    lista_nueva = []


    
    for i, nombre in enumerate(nombres_base):
        notas = [round(random.uniform(5, 20), 1) for _ in range(4)]
        promedio = (notas[0] * 0.1) + (notas[1] * 0.2) + (notas[2] * 0.3) + (notas[3] * 0.4)
        promedio = round(promedio, 2)
        estado = "Aprobado" if promedio >= 11 else "Reprobado"

        Carreras_random = random.choice(Carreras)
        
        est = {
            "id": f"N00{start_id + i:08d}", "nombre": nombre, "carrera": Carreras_random, 
            "n1": notas[0], "n2": notas[1], "n3": notas[2], "n4": notas[3],
            "promedio": promedio, "estado": estado
        }
        lista_nueva.append(est)
    return lista_nueva

# Algoritmo Recursivo: MergeSort (Mérito)
def merge_sort_descendente(lista):
    if len(lista) <= 1: return lista
    medio = len(lista) // 2
    izquierda = merge_sort_descendente(lista[:medio])
    derecha = merge_sort_descendente(lista[medio:])
    return merge(izquierda, derecha)

def merge(izq, der):
    resultado = []
    i = 0; j = 0
    while i < len(izq) and j < len(der):
        if izq[i]['promedio'] > der[j]['promedio']: resultado.append(izq[i]); i += 1
        else: resultado.append(der[j]); j += 1
    resultado.extend(izq[i:]); resultado.extend(der[j:])
    return resultado

# Algoritmo Recursivo: Suma de Promedios
def suma_promedios_recursiva(lista, n):
    if n == 0: return 0
    return lista[n-1]['promedio'] + suma_promedios_recursiva(lista, n-1)

def Conteo_Recursivo_por_Carrera(lista, carrera, n=None):
    if n is None: n = len(lista)
    if n == 0: return 0
    count = Conteo_Recursivo_por_Carrera(lista, carrera, n-1)
    if lista[n-1]['carrera'] == carrera:
        count += 1
    return count

# Inicializamos
estudiantes = generar_datos_random()

root = Tk()
root.title("Sistema Académico Multi-Carrera")
root.geometry("1250x650") # Un poco más ancho para la nueva columna
root.config(bg="#eceff1")

# TOP BAR
top = Frame(root, bg="#0d47a1", height=80)
top.pack(fill="x", side="top")
Label(top, text="🎓 GESTIÓN UNIVERSITARIA", fg="white", bg="#0d47a1", font=("Arial", 22, "bold")).pack(pady=20)

# LOGO AREA
logo_frame = Frame(root, bg="#eceff1")
logo_frame.pack(pady=5)
Label(logo_frame, text="🏛️", bg="#eceff1", fg="#0d47a1", font=("Arial", 40)).pack()

# BODY
body = Frame(root, bg="#eceff1")
body.pack(pady=10)

def tarjeta(parent, color, icono, texto, comando):
    frame = Frame(parent, bg=color, width=150, height=110, bd=0, relief="raised", cursor="hand2")
    frame.pack_propagate(0)
    frame.pack(side="left", padx=8)
    
    for widget in [frame, Label(frame, text=icono, bg=color, fg="white", font=("Arial", 30)), 
                   Label(frame, text=texto, bg=color, fg="white", font=("Arial", 11, "bold"))]:
        if isinstance(widget, Frame): widget.pack_propagate(0)
        else: widget.pack(pady=2 if "Arial 30" in str(widget['font']) else 0)
        widget.bind("<Button-1>", lambda e: comando())
    return frame

# TABLA (Treeview)
panel = Frame(root, bg="white")
panel.pack(fill="both", expand=True, padx=20, pady=10)

# Definimos columnas incluyendo 'carrera'
cols = ("id", "nombre", "carrera", "T1", "T2", "T3", "EF" "promedio", "estado")
tree = ttk.Treeview(panel, columns=cols, show="headings")

headers = ["ID", "Estudiante", "Carrera", "T1", "T2", "T3","EF", "Prom.", "Estado"]
anchos = [50, 200, 180, 50, 50, 50, 60, 90] # Ajuste de anchos

for c, h, w in zip(cols, headers, anchos):
    tree.heading(c, text=h)
    tree.column(c, width=w, anchor="center" if c not in ["nombre", "carrera"] else "w")

scrolly = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrolly.set)
scrolly.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# --- 4. LÓGICA DE INTERACCIÓN ---

def actualizar_tabla(lista_datos=None):
    if lista_datos is None: lista_datos = estudiantes
    for item in tree.get_children(): tree.delete(item)
    for e in lista_datos:
        tree.insert("", "end", values=(e['id'], e['nombre'], e['carrera'], e['n1'], e['n2'], e['n3'], e['promedio'], e['estado']))

def cmd_cambiar_datos():
    global estudiantes
    if estudiantes:
        ultimo_id_num = int(estudiantes[-1]['id'][3:])  # Quitar "N00"
        nuevo_start = ultimo_id_num + 1
    else:
        nuevo_start = 1

    estudiantes = generar_datos_random(start_id=nuevo_start)
    actualizar_tabla()
    messagebox.showinfo("Datos Actualizados", "Se han generado nuevos datos de estudiantes.")

def cmd_reporte():
    if not estudiantes: return
    mejor = max(estudiantes, key=lambda x: x['promedio'])
    peor = min(estudiantes, key=lambda x: x['promedio'])
    
    resumen_carreras = ""
    for carrera in Carreras:
        count = Conteo_Recursivo_por_Carrera(estudiantes, carrera)
        resumen_carreras += f"{carrera}: {count}\n"
    
            
    msg = f"""
    🏆 MEJOR RENDIMIENTO
    Nombre: {mejor['nombre']}
    Carrera: {mejor['carrera']}
    Promedio: {mejor['promedio']}
    
    🏆 PEOR RENDIMIENTO
    Nombre: {peor['nombre']}
    Carrera: {peor['carrera']}
    Promedio: {peor['promedio']}

    ----------------------------------------
    📊 DISTRIBUCIÓN POR CARRERAS (Recursivo)
    ----------------------------------------
    {resumen_carreras}
    """


    messagebox.showinfo("Reporte Avanzado", msg)

def cmd_buscar():
    nombre_buscar = simpledialog.askstring("Buscar Estudiante", "Ingrese el nombre del estudiante:")
    if not nombre_buscar: return
    resultados = [e for e in estudiantes if nombre_buscar.lower() in e['nombre'].lower()]
    if resultados:
        actualizar_tabla(resultados)
    else:
        messagebox.showinfo("No Encontrado", f"No se encontraron estudiantes con el nombre '{nombre_buscar}'.")

def cmd_ordenar():
    global estudiantes
    estudiantes = merge_sort_descendente(estudiantes)
    actualizar_tabla()
    messagebox.showinfo("Ordenado", "Alumnos ordenados por Promedio.")

# --- BOTONES ---
tarjeta(body, "#1565c0", "🎲", "+ Random", cmd_cambiar_datos)
tarjeta(body, "#0277bd", "🥇", "Mérito", cmd_ordenar)
tarjeta(body, "#1e88e5", "🔍", "Buscar", cmd_buscar)
tarjeta(body, "#00838f", "📊", "Reporte", cmd_reporte)
tarjeta(body, "#d32f2f", "🗑️", "Limpiar", lambda: [estudiantes.clear(), actualizar_tabla()])

# Datos iniciales
actualizar_tabla()

root.mainloop()