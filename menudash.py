import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Gestión de Ventas - Dashboard")
root.geometry("1000x600")
root.config(bg="#eceff1")

# ------------------ TOP BAR ---------------------
top = Frame(root, bg="#263238", height=80)
top.pack(fill="x", side="top")

Label(top, text="📊 SISTEMA DE GESTIÓN DE VENTAS",
      fg="white", bg="#263238", font=("Arial", 22, "bold")
      ).pack(pady=20)

# ------------------ IMAGEN / LOGO ---------------------
logo_frame = Frame(root, bg="#eceff1")
logo_frame.pack(pady=20)

try:
    img = Image.open("logo.png")
    img = img.resize((160, 160))
    logo_img = ImageTk.PhotoImage(img)
    Label(logo_frame, image=logo_img, bg="#eceff1").pack()
except:
    Label(logo_frame, text="SIN IMAGEN", bg="#eceff1", fg="gray", font=("Arial", 12)).pack()

# ------------------ BODY / TARJETAS ---------------------

body = Frame(root, bg="#eceff1")
body.pack(pady=20)

def tarjeta(parent, color, icono, texto, comando):
    frame = Frame(parent, bg=color, width=200, height=150, bd=0, relief="raised", cursor="hand2")
    frame.pack_propagate(0)
    frame.pack(side="left", padx=20)

    Label(frame, text=icono, bg=color, fg="white", font=("Arial", 40)).pack(pady=5)
    Label(frame, text=texto, bg=color, fg="white", font=("Arial", 14, "bold")).pack()

    frame.bind("<Button-1>", lambda e: comando())
    return frame

# ------ Acciones de ejemplo ------
def registrar(): cambiar("Registrar productos")
def mostrar(): cambiar("Mostrar productos")
def ordenar(): cambiar("Ordenar productos")
def buscar(): cambiar("Buscar productos")
def reporte(): cambiar("Reporte de ventas")
def total(): cambiar("Cálculo recursivo")

# ------ Panel inferior que cambia ------
panel = Frame(root, bg="white", height=100)
panel.pack(fill="both", expand=True)

label_panel = Label(panel, text="Seleccione una opción del tablero",
                    bg="white", fg="#37474f", font=("Arial", 18))
label_panel.pack(pady=40)

def cambiar(texto):
    label_panel.config(text=texto)

# ------------------ TARJETAS DEL DASHBOARD ---------------------

tarjeta(body, "#546e7a", "📦", "Regitrar", registrar)
tarjeta(body, "#455a64", "📋", "Mostrar", mostrar)
tarjeta(body, "#37474f", "🔃", "Ordenar", ordenar)
tarjeta(body, "#263238", "🔍", "Buscar", buscar)
tarjeta(body, "#1e272e", "📈", "Reporte", reporte)
tarjeta(body, "#000000", "♻️", "Recursivo", total)

root.mainloop()