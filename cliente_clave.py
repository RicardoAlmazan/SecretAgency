import tkinter as tk
from tkinter import simpledialog

class Dialogo:
    def __init__(self):
        self.ventana = tk.Tk()

        canvas = tk.Canvas(self.ventana, width=400, height=300)
        canvas.pack()

        self.respuesta = tk.Entry(self.ventana)
        canvas.create_window(200, 140, window=self.respuesta)

        boton = tk.Button(text='Enviar', command=self.setValueResp)
        canvas.create_window(200, 180, window=boton)

        self.ventana.mainloop()
    
    def setValueResp(self, event=None):
        self.valorRespuesta = self.respuesta.get()
        self.ventana.destroy()
        