import tkinter as tk


class interfaz():
    def __init__(self, send_socket, socket):
        self._send_socket = send_socket
        self._socket = socket

        self.top = tk.Tk()
        self.top.title("Chat - Luis Alamo & Ricardo Almazán")

        self.mensajes_ventana = tk.Frame(self.top)
        self.nuevo_msj = tk.StringVar()

        self.scrollbar = tk.Scrollbar(self.mensajes_ventana)
        self.lista_mensajes = tk.Listbox(
            self.mensajes_ventana, height=25, width=60, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_mensajes.pack(side=tk.LEFT, fill=tk.BOTH)
        self.lista_mensajes.pack()

        self.mensajes_ventana.pack()

        self.mensaje_entrada = tk.Entry(self.top, textvariable=self.nuevo_msj)
        self.mensaje_entrada.bind("<Return>", self.enviar_mensaje)
        self.mensaje_entrada.pack()

        self.boton_enviar = tk.Button(
            self.top, text="Enviar", command=self.enviar_mensaje)
        self.boton_enviar.pack()

        self.lista_mensajes.insert(tk.END, "¡Hola, bienvenido al chat!")
        self.lista_mensajes.insert(
            tk.END, "Escribe tu mensaje en el campo de abajo.")
        self.lista_mensajes.insert(
            tk.END, "Para desconectarte escribe 'salir' o simplemente cierra la ventana.")
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _mostrar(self):
        tk.mainloop()

    def enviar_mensaje(self, event=None):
        mensaje = self.nuevo_msj.get()
        self.lista_mensajes.insert(tk.END, "Yo: " + mensaje)
        self.nuevo_msj.set("")
        self._send_socket(mensaje)
        if(mensaje.lower() == "salir"):
            self._socket.close()
            self.top.quit()

    def mensaje_recibido(self, mensaje):
        self.lista_mensajes.insert(tk.END, mensaje)

    def on_closing(self, event=None):
        self.nuevo_msj.set("salir")
        self.enviar_mensaje()
