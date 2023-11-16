import socket
import sys
import threading

def recibir_mensajes(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"\n\t\t\t\t\t",data.decode('utf-8'))
        except ConnectionResetError:
            print("Conexión con el servidor cerrada.")
            break

def main():
    arguments = sys.argv
    if len(arguments) != 2:
        print(f"Uso: python clienteTCP.py <host>")
        exit(1)

    host = arguments[1]
    port_tcp = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port_tcp))
    print(f"Conectado al servidor TCP en {host}:{port_tcp}")

    nombre_usuario = input("Ingrese su nombre de usuario: ").lower()
    client_socket.send(nombre_usuario.encode('utf-8'))

    # Crear un hilo para recibir mensajes del servidor
    threading.Thread(target=recibir_mensajes, args=(client_socket,), daemon=True).start()

    while True:
        destinatario = input("Ingrese el nombre del destinatario (o 'exit' para salir): ").lower()
        if destinatario == 'exit':
            break

        message = input("Ingrese un mensaje: ")
        client_socket.send(f"{destinatario}:{message}".encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()
