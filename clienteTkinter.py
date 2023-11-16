import socket
import sys
import threading
import tkinter as tk
from tkinter import scrolledtext

class ClienteTkinter:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.root = tk.Tk()
        self.root.title("Cliente TCP")

        self.nombre_usuario = ""
        self.destinatario = ""
        self.mensaje = ""

        self.iniciar_interfaz()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        threading.Thread(target=self.recibir_nombre, daemon=True).start()

    def iniciar_interfaz(self):
        self.etiqueta_nombre = tk.Label(self.root, text="Nombre:")
        self.etiqueta_nombre.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.entrada_nombre = tk.Entry(self.root, width=20)
        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=5)

        self.boton_ingresar = tk.Button(self.root, text="Ingresar", command=self.ingresar_nombre)
        self.boton_ingresar.grid(row=0, column=2, padx=10, pady=5)

        self.chat_text = scrolledtext.ScrolledText(self.root, width=40, height=10, state=tk.DISABLED)
        self.chat_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.etiqueta_destinatario = tk.Label(self.root, text="Destinatario:")
        self.etiqueta_destinatario.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.entrada_destinatario = tk.Entry(self.root, width=20)
        self.entrada_destinatario.grid(row=2, column=1, padx=10, pady=5)

        self.etiqueta_mensaje = tk.Label(self.root, text="Mensaje:")
        self.etiqueta_mensaje.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        self.entrada_mensaje = tk.Entry(self.root, width=20)
        self.entrada_mensaje.grid(row=3, column=1, padx=10, pady=5)

        self.boton_enviar = tk.Button(self.root, text="Enviar Mensaje", command=self.enviar_mensaje)
        self.boton_enviar.grid(row=3, column=2, padx=10, pady=5)

    def ingresar_nombre(self):
        self.nombre_usuario = self.entrada_nombre.get().lower()
        if self.nombre_usuario:
            self.client_socket.send(self.nombre_usuario.encode('utf-8'))
            self.entrada_nombre.config(state=tk.DISABLED)
            self.boton_ingresar.config(state=tk.DISABLED)

            threading.Thread(target=self.recibir_mensajes, daemon=True).start()

    def enviar_mensaje(self):
        self.destinatario = self.entrada_destinatario.get().lower()
        self.mensaje = self.entrada_mensaje.get()

        if self.destinatario and self.mensaje:
            mensaje_enviar = f"{self.destinatario}: {self.nombre_usuario}: {self.mensaje}"
            self.client_socket.send(mensaje_enviar.encode('utf-8'))

            self.entrada_destinatario.delete(0, tk.END)
            self.entrada_mensaje.delete(0, tk.END)

    def recibir_mensajes(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                mensaje = data.decode('utf-8')
                self.mostrar_mensaje(mensaje)
            except ConnectionResetError:
                print("Conexión con el servidor cerrada.")
                break

    def recibir_nombre(self):
        data = self.client_socket.recv(1024)
        self.nombre_usuario = data.decode('utf-8')
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, self.nombre_usuario.lower())
        self.entrada_nombre.config(state=tk.DISABLED)
        self.boton_ingresar.config(state=tk.DISABLED)

        threading.Thread(target=self.recibir_mensajes, daemon=True).start()

    def mostrar_mensaje(self, mensaje):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, mensaje + '\n')
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 2:
        print(f"Uso: python clienteTkinter.py <host>")
        exit(1)

    host = arguments[1]
    port_tcp = 5000

    cliente_tkinter = ClienteTkinter(host, port_tcp)
    cliente_tkinter.ejecutar()
