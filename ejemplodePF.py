import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk

# --- 1. LÓGICA Y DATOS (BACKEND) ---

inventario = [
    {"id": 1, "nombre": "Laptop Gamer", "precio": 1200.0, "stock": 5},
    {"id": 2, "nombre": "Mouse Optico", "precio": 25.0, "stock": 50},
    {"id": 3, "nombre": "Teclado Mecanico", "precio": 85.0, "stock": 20},
    {"id": 4, "nombre": "Monitor 24in", "precio": 180.0, "stock": 10},
]

# Algoritmo Recursivo 1: QuickSort
def quicksort_recursivo(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]['precio']
    izquierda = [x for x in lista if x['precio'] < pivote]
    medio = [x for x in lista if x['precio'] == pivote]
    derecha = [x for x in lista if x['precio'] > pivote]
    return quicksort_recursivo(izquierda) + medio + quicksort_recursivo(derecha)

# Algoritmo Recursivo 2: Suma de Valor de Inventario
def suma_recursiva(lista, n):
    if n == 0:
        return 0
    actual = lista[n-1]['precio'] * lista[n-1]['stock']
    return actual + suma_recursiva(lista, n-1)

# --- 2. INTERFAZ GRÁFICA (FRONTEND) ---

root = Tk()
root.title("Gestión de Ventas - Dashboard")
root.geometry("1100x650") # Un poco más ancho para que quepan los botones
root.config(bg="#eceff1")

# ------------------ TOP BAR ---------------------
top = Frame(root, bg="#263238", height=80)
top.pack(fill="x", side="top")

Label(top, text="📊 SISTEMA DE GESTIÓN DE VENTAS",
      fg="white", bg="#263238", font=("Arial", 22, "bold")
      ).pack(pady=20)

# ------------------ IMAGEN / LOGO ---------------------
logo_frame = Frame(root, bg="#eceff1")
logo_frame.pack(pady=10)

try:
    # Asegúrate de tener una imagen llamada 'logo.png' o el bloque except se activará
    img = Image.open("logo.png")
    img = img.resize((100, 100)) # Reduje un poco el logo para dar espacio
    logo_img = ImageTk.PhotoImage(img)
    Label(logo_frame, image=logo_img, bg="#eceff1").pack()
except:
    Label(logo_frame, text="[SISTEMA PY]", bg="#eceff1", fg="gray", font=("Arial", 20, "bold")).pack()

# ------------------ BODY / TARJETAS ---------------------

body = Frame(root, bg="#eceff1")
body.pack(pady=10)

def tarjeta(parent, color, icono, texto, comando):
    frame = Frame(parent, bg=color, width=160, height=130, bd=0, relief="raised", cursor="hand2")
    frame.pack_propagate(0)
    frame.pack(side="left", padx=10) # Reduje padx para que quepan todos

    Label(frame, text=icono, bg=color, fg="white", font=("Arial", 35)).pack(pady=5)
    Label(frame, text=texto, bg=color, fg="white", font=("Arial", 12, "bold")).pack()

    # Bind al frame y a los labels internos para que funcione al hacer click en cualquier parte
    frame.bind("<Button-1>", lambda e: comando())
    for widget in frame.winfo_children():
        widget.bind("<Button-1>", lambda e: comando())
        
    return frame

# ------------------ PANEL INFERIOR (TABLA) ---------------------
panel = Frame(root, bg="white")
panel.pack(fill="both", expand=True, padx=20, pady=20)

# Configuración del Treeview (Tabla)
style = ttk.Style()
style.configure("Treeview", font=("Arial", 11), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

columns = ("id", "nombre", "precio", "stock")
tree = ttk.Treeview(panel, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("nombre", text="Producto")
tree.heading("precio", text="Precio ($)")
tree.heading("stock", text="Stock")

tree.column("id", width=50, anchor="center")
tree.column("nombre", width=300)
tree.column("precio", width=100, anchor="center")
tree.column("stock", width=100, anchor="center")

# Scrollbar
scrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# --- 3. FUNCIONES DE LOS BOTONES ---

def actualizar_tabla(lista_datos=None):
    """Limpia la tabla y la llena con los datos recibidos"""
    if lista_datos is None:
        lista_datos = inventario
        
    # Limpiar tabla
    for item in tree.get_children():
        tree.delete(item)
    
    # Llenar tabla
    for prod in lista_datos:
        tree.insert("", "end", values=(prod['id'], prod['nombre'], prod['precio'], prod['stock']))

def cmd_mostrar():
    actualizar_tabla(inventario)

def cmd_registrar():
    # Ventanas simples para pedir datos
    nombre = simpledialog.askstring("Nuevo", "Nombre del producto:")
    if nombre:
        try:
            precio = float(simpledialog.askstring("Nuevo", "Precio:"))
            stock = int(simpledialog.askstring("Nuevo", "Stock inicial:"))
            nuevo_id = len(inventario) + 101 # Generar ID simple
            
            nuevo_prod = {"id": nuevo_id, "nombre": nombre, "precio": precio, "stock": stock}
            inventario.append(nuevo_prod)
            actualizar_tabla()
            messagebox.showinfo("Éxito", "Producto registrado correctamente")
        except:
            messagebox.showerror("Error", "Datos numéricos inválidos")

def cmd_ordenar():
    # Usa la función recursiva quicksort
    global inventario
    inventario = quicksort_recursivo(inventario)
    actualizar_tabla()
    messagebox.showinfo("Ordenamiento", "Productos ordenados por PRECIO (Recursivo QuickSort)")

def cmd_buscar():
    termino = simpledialog.askstring("Buscar", "Nombre del producto a buscar:")
    if termino:
        # Búsqueda lineal
        resultados = [p for p in inventario if termino.lower() in p['nombre'].lower()]
        if resultados:
            actualizar_tabla(resultados)
        else:
            messagebox.showwarning("Buscar", "No se encontraron coincidencias")
            actualizar_tabla(inventario) # Restaurar vista

def cmd_reporte():
    if not inventario: return
    # Uso de lambdas para cálculos rápidos
    mas_caro = max(inventario, key=lambda x: x['precio'])
    mas_barato = min(inventario, key=lambda x: x['precio'])
    
    msg = f"""
    REPORTE ESTADÍSTICO
    -------------------
    Total Productos: {len(inventario)}
    
    💎 Más caro: {mas_caro['nombre']} (${mas_caro['precio']})
    📉 Más barato: {mas_barato['nombre']} (${mas_barato['precio']})
    """
    messagebox.showinfo("Reporte", msg)

def cmd_total():
    # Usa la función recursiva de suma
    total = suma_recursiva(inventario, len(inventario))
    messagebox.showinfo("Cálculo Recursivo", f"El valor total del inventario es:\n\n💰 ${total:,.2f}")

# ------------------ CREACIÓN DE TARJETAS ---------------------
# NOTA: Pasamos las funciones 'cmd_' sin paréntesis

tarjeta(body, "#546e7a", "📦", "Registrar", cmd_registrar)
tarjeta(body, "#455a64", "📋", "Mostrar", cmd_mostrar)
tarjeta(body, "#37474f", "🔃", "Ordenar", cmd_ordenar)
tarjeta(body, "#263238", "🔍", "Buscar", cmd_buscar)
tarjeta(body, "#1e272e", "📈", "Reporte", cmd_reporte)
tarjeta(body, "#000000", "♻️", "V. Total", cmd_total)

# Cargar datos iniciales
actualizar_tabla()

root.mainloop()