import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# ---------------- VENTANA PRINCIPAL ------------------
root = Tk()
root.title("Gestión de Ventas - UPN")
root.geometry("900x550")
root.config(bg="#f4f4f4")

# ---------------- SIDEBAR IZQUIERDO ------------------
sidebar = Frame(root, bg="#1f2937", width=250)
sidebar.pack(fill="y", side="left")

# Imagen en la parte superior
try:
    logo = Image.open("logo.png")
    logo = logo.resize((140, 140))
    logo_img = ImageTk.PhotoImage(logo)
    Label(sidebar, image=logo_img, bg="#1f2937").pack(pady=20)
except:
    Label(sidebar, text="SIN IMAGEN", fg="white", bg="#1f2937").pack(pady=20)

# Título
Label(sidebar, text="MENÚ PRINCIPAL", font=("Arial", 14, "bold"), fg="white", bg="#1f2937").pack(pady=10)

# Template para botones
def crear_boton(texto, comando):
    return Button(
        sidebar, text=texto, command=comando,
        bg="#374151", fg="white",
        font=("Arial", 12, "bold"),
        activebackground="#4b5563",
        relief="flat", cursor="hand2",
        width=20, pady=10
    )

# Botones de menú
crear_boton("Registrar productos", lambda: mostrar("Registrar productos")).pack(pady=5)
crear_boton("Mostrar productos", lambda: mostrar("Mostrar productos")).pack(pady=5)
crear_boton("Ordenar productos", lambda: mostrar("Ordenar productos")).pack(pady=5)
crear_boton("Buscar productos", lambda: mostrar("Buscar productos")).pack(pady=5)
crear_boton("Reporte de ventas", lambda: mostrar("Reporte de ventas")).pack(pady=5)
crear_boton("Cálculo recursivo", lambda: mostrar("Cálculo recursivo")).pack(pady=5)
crear_boton("Salir", root.quit).pack(pady=30)

# ---------------- PANEL PRINCIPAL ------------------
panel = Frame(root, bg="white")
panel.pack(fill="both", expand=True)

label_panel = Label(panel, text="Bienvenido al Sistema de Gestión de Ventas",
                    font=("Arial", 20, "bold"), fg="#333", bg="white")
label_panel.pack(pady=40)

def mostrar(texto):
    label_panel.config(text=texto)

root.mainloop()