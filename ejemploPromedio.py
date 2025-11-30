import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import random


estudiantes = []

def generar_datos_random():
    nombres_base = ["Ana Torres", "Carlos Ruiz", "Elena Gomez", "David Gil", 
                    "Beatriz Lima", "Fernando Solis", "Gloria Mendez", "Hugo Chavez"]
    lista_nueva = []
    start_id = 101
    
    for i, nombre in enumerate(nombres_base):
        notas = [round(random.uniform(5, 20), 1) for _ in range(3)]
        promedio = round(sum(notas) / len(notas), 2)
        estado = "Aprobado" if promedio >= 11 else "Reprobado"
        
        est = {
            "id": start_id + i, "nombre": nombre, 
            "n1": notas[0], "n2": notas[1], "n3": notas[2],
            "promedio": promedio, "estado": estado
        }
        lista_nueva.append(est)
    return lista_nueva

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

def suma_promedios_recursiva(lista, n):
    if n == 0: return 0
    return lista[n-1]['promedio'] + suma_promedios_recursiva(lista, n-1)

estudiantes = generar_datos_random()

# --- 2. INTERFAZ GRÁFICA ---

root = Tk()
root.title("Sistema de Gestión Académica")
root.geometry("1150x650")
root.config(bg="#eceff1")

# TOP BAR
top = Frame(root, bg="#1a237e", height=80)
top.pack(fill="x", side="top")
Label(top, text="🎓 SISTEMA DE NOTAS Y REGISTRO", fg="white", bg="#1a237e", font=("Arial", 22, "bold")).pack(pady=20)

# LOGO
logo_frame = Frame(root, bg="#eceff1")
logo_frame.pack(pady=5)
try:
    img = Image.open("logo.png").resize((70, 70))
    logo_img = ImageTk.PhotoImage(img)
    Label(logo_frame, image=logo_img, bg="#eceff1").pack()
except:
    Label(logo_frame, text="🏛️", bg="#eceff1", fg="#1a237e", font=("Arial", 40)).pack()

# BODY (CONTENEDOR DE TARJETAS)
body = Frame(root, bg="#eceff1")
body.pack(pady=10)

def tarjeta(parent, color, icono, texto, comando):
    frame = Frame(parent, bg=color, width=140, height=110, bd=0, relief="raised", cursor="hand2")
    frame.pack_propagate(0)
    frame.pack(side="left", padx=8)
    
    lbl_icon = Label(frame, text=icono, bg=color, fg="white", font=("Arial", 30))
    lbl_icon.pack(pady=5)
    lbl_text = Label(frame, text=texto, bg=color, fg="white", font=("Arial", 11, "bold"))
    lbl_text.pack()

    # Hacemos que todo el cuadro sea clickeable
    for widget in (frame, lbl_icon, lbl_text):
        widget.bind("<Button-1>", lambda e: comando())
    return frame

# TABLA
panel = Frame(root, bg="white")
panel.pack(fill="both", expand=True, padx=20, pady=10)

columnas = ("id", "nombre", "n1", "n2", "n3", "promedio", "estado")
tree = ttk.Treeview(panel, columns=columnas, show="headings", height=10)

headers = ["ID", "Estudiante", "Nota 1", "Nota 2", "Nota 3", "Promedio", "Estado"]
anchos = [50, 250, 60, 60, 60, 80, 100]

for col, head, ancho in zip(columnas, headers, anchos):
    tree.heading(col, text=head)
    tree.column(col, width=ancho, anchor="center" if col != "nombre" else "w")

scrolly = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrolly.set)
scrolly.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# --- 3. FUNCIONES DE INTERACCIÓN ---

def actualizar_tabla(lista_datos=None):
    if lista_datos is None: lista_datos = estudiantes
    for item in tree.get_children(): tree.delete(item)
    for est in lista_datos:
        tree.insert("", "end", values=(est['id'], est['nombre'], est['n1'], est['n2'], est['n3'], est['promedio'], est['estado']))

# --- NUEVA FUNCIÓN: REGISTRAR ALUMNO ---
def cmd_nuevo_alumno():
    # Ventana personalizada (TopLevel)
    ventana_reg = Toplevel(root)
    ventana_reg.title("Nuevo Alumno")
    ventana_reg.geometry("300x350")
    ventana_reg.config(bg="#f5f5f5")
    ventana_reg.grab_set() # Bloquea la ventana principal hasta cerrar esta

    Label(ventana_reg, text="Datos del Alumno", bg="#f5f5f5", font=("Arial", 12, "bold")).pack(pady=10)

    # Entradas
    entries = {}
    campos = ["Nombre Completo", "Nota 1 (0-20)", "Nota 2 (0-20)", "Nota 3 (0-20)"]
    
    for campo in campos:
        frame_campo = Frame(ventana_reg, bg="#f5f5f5")
        frame_campo.pack(pady=5, padx=20, fill="x")
        Label(frame_campo, text=campo, bg="#f5f5f5", anchor="w").pack(fill="x")
        entry = Entry(frame_campo)
        entry.pack(fill="x")
        entries[campo] = entry

    def guardar():
        try:
            nombre = entries["Nombre Completo"].get()
            n1 = float(entries["Nota 1 (0-20)"].get())
            n2 = float(entries["Nota 2 (0-20)"].get())
            n3 = float(entries["Nota 3 (0-20)"].get())

            if not nombre: raise ValueError("Nombre vacío")
            if not (0 <= n1 <= 20 and 0 <= n2 <= 20 and 0 <= n3 <= 20):
                messagebox.showerror("Error", "Las notas deben estar entre 0 y 20")
                return

            # Calcular datos
            prom = round((n1 + n2 + n3) / 3, 2)
            estado = "Aprobado" if prom >= 11 else "Reprobado"
            
            # Generar ID (El máximo actual + 1)
            nuevo_id = max(e['id'] for e in estudiantes) + 1 if estudiantes else 101
            
            nuevo_estudiante = {
                "id": nuevo_id, "nombre": nombre, 
                "n1": n1, "n2": n2, "n3": n3,
                "promedio": prom, "estado": estado
            }
            
            estudiantes.append(nuevo_estudiante)
            actualizar_tabla()
            ventana_reg.destroy()
            messagebox.showinfo("Éxito", f"Alumno {nombre} registrado correctamente.")
            
        except ValueError:
            messagebox.showerror("Error", "Revise los datos ingresados.\nLas notas deben ser números.")

    Button(ventana_reg, text="GUARDAR", bg="#4caf50", fg="white", command=guardar).pack(pady=20, fill="x", padx=20)

def cmd_regenerar():
    global estudiantes
    estudiantes = generar_datos_random()
    actualizar_tabla()

def cmd_ordenar():
    global estudiantes
    estudiantes = merge_sort_descendente(estudiantes)
    actualizar_tabla()
    messagebox.showinfo("Ordenado", "Lista ordenada por Mérito (MergeSort)")

def cmd_buscar():
    nombre = simpledialog.askstring("Buscar", "Nombre del estudiante:")
    if nombre:
        res = [e for e in estudiantes if nombre.lower() in e['nombre'].lower()]
        if res: actualizar_tabla(res)
        else: messagebox.showwarning("Error", "No encontrado"); actualizar_tabla()

def cmd_reporte():
    if not estudiantes: return
    aprobados = len([e for e in estudiantes if e['promedio'] >= 11])
    mejor = max(estudiantes, key=lambda x: x['promedio'])
    messagebox.showinfo("Reporte", f"Total: {len(estudiantes)}\nAprobados: {aprobados}\nMejor: {mejor['nombre']} ({mejor['promedio']})")

def cmd_prom_recursivo():
    if not estudiantes: return
    suma = suma_promedios_recursiva(estudiantes, len(estudiantes))
    messagebox.showinfo("Recursividad", f"Promedio del Salón: {suma/len(estudiantes):.2f}")

# --- BOTONES ---
tarjeta(body, "#4caf50", "➕", "Nuevo", cmd_nuevo_alumno)
tarjeta(body, "#283593", "🎲", "Random", cmd_regenerar)
tarjeta(body, "#3949ab", "📋", "Todo", lambda: actualizar_tabla(estudiantes))
tarjeta(body, "#303f9f", "🥇", "Mérito", cmd_ordenar)
tarjeta(body, "#1e88e5", "🔍", "Buscar", cmd_buscar)
tarjeta(body, "#0277bd", "📊", "Reporte", cmd_reporte)
tarjeta(body, "#006064", "➗", "Promedio", cmd_prom_recursivo)

actualizar_tabla()
root.mainloop()