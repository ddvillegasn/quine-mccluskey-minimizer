import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math

# Funciones del algoritmo de McCluskey
def contar_bits_uno(num):
    return bin(num).count('1')

def convertir_a_binario(num, longitud):
    return bin(num)[2:].zfill(longitud)

def combinar_tiempos(t1, t2):
    combinado, diferencias = "", 0
    for i in range(len(t1)):
        if t1[i] != t2[i]:
            combinado += "-"
            diferencias += 1
        else:
            combinado += t1[i]
    return combinado if diferencias == 1 else None

def traducir_implicante(implicante, num_vars):
    vars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_vars]
    expresion = []
    for i, bit in enumerate(implicante):
        if bit == '1':
            expresion.append(vars[i])
        elif bit == '0':
            expresion.append(vars[i] + "'")
    return ''.join(expresion)

def metodo_mccluskey(minterms):
    num_vars = math.ceil(math.log2(max(minterms) + 1))
    grupos = {}
    for minterm in minterms:
        bin_term = convertir_a_binario(minterm, num_vars)
        uno_count = contar_bits_uno(minterm)
        if uno_count not in grupos:
            grupos[uno_count] = []
        grupos[uno_count].append(bin_term)
    
    implicantes_primos = set()
    verificados = set()
    
    while True:
        nuevos_grupos, combinaciones = {}, False
        for i in range(len(grupos)):
            if i in grupos and i + 1 in grupos:
                for t1 in grupos[i]:
                    for t2 in grupos[i + 1]:
                        combinado = combinar_tiempos(t1, t2)
                        if combinado:
                            combinaciones = True
                            verificados.update([t1, t2])
                            cuenta_unos = combinado.count('1')
                            if cuenta_unos not in nuevos_grupos:
                                nuevos_grupos[cuenta_unos] = []
                            if combinado not in nuevos_grupos[cuenta_unos]:
                                nuevos_grupos[cuenta_unos].append(combinado)

        for grupo in grupos.values():
            for term in grupo:
                if term not in verificados:
                    implicantes_primos.add(term)

        if not combinaciones:
            break
        
        grupos = nuevos_grupos

    implicantes_primarios_esenciales = []
    minterms_no_cubiertos = set(minterms)
    tabla = {imp: set() for imp in implicantes_primos}

    for minterm in minterms:
        bin_term = convertir_a_binario(minterm, num_vars)
        for imp in implicantes_primos:
            if all(x == y or x == '-' for x, y in zip(imp, bin_term)):
                tabla[imp].add(minterm)

    while minterms_no_cubiertos:
        if not tabla:
            return None
        # Elegir el implicante que cubre más minterms no cubiertos
        mejor_implicante = max(tabla, key=lambda imp: len(tabla[imp] & minterms_no_cubiertos))
        implicantes_primarios_esenciales.append(mejor_implicante)
        cubiertos = tabla[mejor_implicante]
        minterms_no_cubiertos -= cubiertos

        # Eliminar implicantes que ya no cubren minterms no cubiertos
        tabla = {imp: cubre for imp, cubre in tabla.items() if cubre & minterms_no_cubiertos}

    resultado = [traducir_implicante(imp, num_vars) for imp in implicantes_primarios_esenciales]
    return resultado, num_vars

# Funciones para la interfaz gráfica
def calcular_resultado():
    try:
        minterms = list(map(int, entry_minterms.get().split()))
        resultado, num_vars = metodo_mccluskey(minterms)
        resultado_str = ' + '.join(resultado) if resultado else None
        result_label.config(
            text=f"Número de variables: {num_vars}\nImplicantes esenciales:\n{resultado_str if resultado_str else '1'}",
            foreground="#333333"
        )
    except ValueError:
        result_label.config(
            text="Error: Entrada inválida. Por favor, ingrese minterms separados por espacio.",
            foreground="#D32F2F"
        )

def limpiar_campos():
    entry_minterms.delete(0, tk.END)
    result_label.config(text="")

def cerrar_aplicacion():
    root.destroy()

# Crear la ventana principal de la interfaz gráfica
root = tk.Tk()
root.title("Simplificación de McCluskey")
root.geometry("800x600")
root.config(bg="#F0F0F0")

# Estilo de fuente
fuente_titulo = ("Segoe UI", 22, "bold")
fuente_botones = ("Segoe UI", 14, "bold")
fuente_resultados = ("Segoe UI", 12)

# Encabezado
titulo = tk.Label(root, text="Método de McCluskey", font=fuente_titulo, bg="#2196F3", fg="#FFFFFF", padx=20, pady=20)
titulo.pack(fill=tk.X)

# Etiqueta para el campo de entrada
etiqueta_minterms = tk.Label(root, text="Introduce los minterms separados por espacio:", font=fuente_botones, bg="#F0F0F0", fg="#333333")
etiqueta_minterms.pack(pady=10)

# Campo de entrada
entry_minterms = tk.Entry(root, width=50, font=("Segoe UI", 14))
entry_minterms.pack(pady=10)

# Frame para los botones
frame_botones = tk.Frame(root, bg="#F0F0F0")
frame_botones.pack(pady=20)

# Botones con estilo moderno
btn_calcular = ttk.Button(frame_botones, text="Calcular", command=calcular_resultado)
btn_calcular.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
btn_calcular.config(style='TButton')

btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos)
btn_limpiar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
btn_limpiar.config(style='TButton')

btn_salir = ttk.Button(frame_botones, text="Salir", command=cerrar_aplicacion)
btn_salir.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
btn_salir.config(style='TButton')

# Etiqueta para mostrar resultados
result_label = tk.Label(root, text="", font=fuente_resultados, bg="#F0F0F0", fg="#333333")
result_label.pack(pady=20)

# Frame para las imágenes
frame_imagenes = tk.Frame(root, bg="#F0F0F0")
frame_imagenes.pack(pady=20)

# Cargar y mostrar la primera imagen
imagen1 = Image.open("Foto.png")
imagen1 = imagen1.resize((300, 200), Image.LANCZOS)  # Ajusta el tamaño de la imagen si es necesario
imagen_tk1 = ImageTk.PhotoImage(imagen1)
foto_label1 = tk.Label(frame_imagenes, image=imagen_tk1, bg="#F0F0F0")
foto_label1.pack(side=tk.LEFT, padx=10)

# Cargar y mostrar la segunda imagen
imagen2 = Image.open("Molly.png")
imagen2 = imagen2.resize((300, 200), Image.LANCZOS)  # Ajusta el tamaño de la imagen si es necesario
imagen_tk2 = ImageTk.PhotoImage(imagen2)
foto_label2 = tk.Label(frame_imagenes, image=imagen_tk2, bg="#F0F0F0")
foto_label2.pack(side=tk.LEFT, padx=10)

# Aplicar estilos a los botones
style = ttk.Style()
style.configure('TButton', font=fuente_botones, padding=10, background="#4CAF50", foreground="white")
style.map('TButton',
          background=[('active', '#45A049')],
          foreground=[('active', 'white')])

# Ejecutar la interfaz gráfica
root.mainloop()