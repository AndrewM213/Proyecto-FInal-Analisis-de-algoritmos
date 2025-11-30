import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

def registrar_productos():
    print("Registrar productos…")

def mostrar_productos():
    print("Mostrar productos…")

def ordenar_productos():
    print("Ordenar productos…")

def buscar_productos():
    print("Buscar productos…")

def reporte_ventas():
    print("Reporte de ventas…")

def calcular_total():
    print("Calcular total recursivo…")

# Ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Ventas")
root.geometry("800x500")
root.config(bg="#f2f2f2")

# Cargar imagen PNG
imagen = Image.open("logo.png")   # Reemplazar con tu PNG
imagen = imagen.resize((250, 250))
img = ImageTk.PhotoImage(imagen)

# Panel izquierdo con la imagen
panel_img = Label(root, image=img, bg="#f2f2f2")
panel_img.pack(side="left", padx=20, pady=20)

# Panel derecho con el menú

panel_menu = Frame(root, bg="#f2f2f2")
panel_menu.pack(side="right", padx=40)

titulo = Label(panel_menu, text="MENÚ PRINCIPAL", font=("Arial", 20, "bold"), bg="#f2f2f2")
titulo.pack(pady=10)

# Botones de menú
botones = [
    ("Registrar productos", registrar_productos),
    ("Mostrar productos", mostrar_productos),
    ("Ordenar productos", ordenar_productos),
    ("Buscar productos", buscar_productos),
    ("Reporte de ventas", reporte_ventas),
    ("Calcular total (recursivo)", calcular_total),
    ("Salir", root.quit),
]

for texto, accion in botones:
    boton = Button(
        panel_menu, 
        text=texto, 
        command=accion,
        width=25, 
        height=2, 
        bg="#4a90e2", 
        fg="white", 
        font=("Arial", 12, "bold")
    )
    boton.pack(pady=5)

root.mainloop()