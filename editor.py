import tkinter as tk
import json
import os
from tkinter import filedialog, messagebox, font, colorchooser, ttk

class SimpleTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PandaStudio")
        self.root.geometry("800x600")
        #self.current_font = ("Pet Me 2Y", 18)
        
        self.wrap_activado = False
        self.cargar_configuracion_fuente() #Mantener la ultima configuración 


        self.text_area = tk.Text(root, wrap="word", font=self.current_font, bg=self.bg_color, fg=self.fg_color)
        self.text_area.pack(fill="both", expand=True)

        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        self.create_menus()

    def create_menus(self):
        # Archivo
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.nuevo)
        file_menu.add_command(label="Abrir", command=self.abrir)
        file_menu.add_command(label="Guardar", command=self.guardar)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        self.menu.add_cascade(label="Archivo", menu=file_menu)

        # Personalizar
        custom_menu = tk.Menu(self.menu, tearoff=0)
        custom_menu.add_command(label="Cambiar fuente", command=self.cambiar_fuente)
        custom_menu.add_command(label="Cambiar color de texto", command=self.cambiar_color_texto)
        custom_menu.add_command(label="Cambiar fondo", command=self.cambiar_color_fondo)
        self.menu.add_cascade(label="Personalizar", menu=custom_menu)
        custom_menu.add_checkbutton(label="Ajuste de línea", command=self.alternar_ajuste_linea, onvalue=True, offvalue=False)


    def nuevo(self):
        self.text_area.delete(1.0, tk.END)

    def abrir(self):
        archivo = filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())

    def guardar(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Guardado", "Archivo guardado correctamente.")

    def cambiar_fuente(self):
        ventana_fuente = tk.Toplevel(self.root)
        ventana_fuente.title("Cambiar fuente")
        ventana_fuente.geometry("300x200")

        fuentes = list(font.families())
        fuentes.sort()

        tk.Label(ventana_fuente, text="Fuente:").pack(pady=5)
        fuente_var = tk.StringVar(value=self.current_font[0])
        fuente_combo = ttk.Combobox(ventana_fuente, textvariable=fuente_var, values=fuentes, state="readonly")
        fuente_combo.pack()

        tk.Label(ventana_fuente, text="Tamaño:").pack(pady=5)
        tamaño_var = tk.StringVar(value=str(self.current_font[1]))
        tamaño_entrada = tk.Entry(ventana_fuente, textvariable=tamaño_var)
        tamaño_entrada.pack()

        def aplicar():
            fuente = fuente_combo.get()
            try:
                tamaño = int(tamaño_var.get())
                self.current_font = (fuente, tamaño)
                self.text_area.config(font=self.current_font)
                self.guardar_configuracion_fuente()

                ventana_fuente.destroy()
            except ValueError:
                messagebox.showerror("Error", "El tamaño debe ser un número.")

        tk.Button(ventana_fuente, text="Aplicar", command=aplicar).pack(pady=10)

    def cambiar_color_texto(self):
        color = colorchooser.askcolor(title="Elige un color de texto")[1]
        if color:
            self.text_area.config(fg=color)
            self.guardar_configuracion_fuente()


    def cambiar_color_fondo(self):
        color = colorchooser.askcolor(title="Elige un color de fondo")[1]
        if color:
            self.text_area.config(bg=color)
            self.guardar_configuracion_fuente()


    def alternar_ajuste_linea(self):
    	self.wrap_activado = not self.wrap_activado
    	nuevo_wrap = "word" if self.wrap_activado else "none"
    	self.text_area.config(wrap=nuevo_wrap)

    def guardar_configuracion_fuente(self):
        config = {
            "fuente": self.current_font[0],
            "tamaño": self.current_font[1],
            "color_fondo": self.text_area["bg"],
            "color_texto": self.text_area["fg"]
        }
        with open("config_fuente.json", "w", encoding="utf-8") as f:
            json.dump(config, f)

    def cargar_configuracion_fuente(self):
        if os.path.exists("config_fuente.json"):
                try:
                    with open("config_fuente.json", "r", encoding="utf-8") as f:
                        config = json.load(f)
                        fuente = config.get("fuente", "Pet Me 2Y")
                        tamaño = config.get("tamaño", 18)
                        self.current_font = (fuente, tamaño)
                        self.bg_color = config.get("color_fondo", "black")
                        self.fg_color = config.get("color_texto", "salmon")

                except Exception as e:
                    print("Error al cargar configuración:", e)
                    self.current_font = ("Arial", 12)
        else:
                self.current_font = ("Arial", 12)



if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleTextEditor(root)
    root.mainloop()
