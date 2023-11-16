import socket
import threading
import sys

clientes_tcp = {}
clientes_udp = {}

def handle_tcp_client(client_socket, client_address):
    try:
        # Obtener el nombre del cliente TCP
        nombre_cliente = client_socket.recv(1024).decode('utf-8').lower()
        clientes_tcp[nombre_cliente] = client_socket

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            print(f"Mensaje recibido: {data.decode('utf-8')}")
            destinatario, mensaje = map(str.lower, data.decode('utf-8').split(':', 1))

            if destinatario in map(str.lower, clientes_tcp):
                destinatario_socket = clientes_tcp[destinatario]
                mensaje_enviar = f"{nombre_cliente}: {mensaje}"
                destinatario_socket.send(mensaje_enviar.encode('utf-8'))
            else:
                print(f"Error: El cliente {destinatario} no existe.")

    except ConnectionResetError:
        print(f"Conexión TCP con {client_address} cerrada por el cliente.")
    finally:
        del clientes_tcp[nombre_cliente]
        client_socket.close()


def handle_udp_client(server_socket_udp):
    while True:
        data, client_address = server_socket_udp.recvfrom(1024)

        # Obtener el nombre del cliente
        nombre_cliente, mensaje = data.decode('utf-8').split(':', 1)

        # Enviar el mensaje a todos los clientes UDP
        for nombre, addr in clientes_udp.items():
            if nombre != nombre_cliente:
                mensaje_enviar = f"{nombre_cliente}: {mensaje}"
                server_socket_udp.sendto(mensaje_enviar.encode('utf-8'), addr)

def main():
    arguments = sys.argv
    if len(arguments) != 3:
        print(f"Uso: python servidor.py <host> <numero_conexiones>")
        exit(1)

    host = arguments[1]
    nConexiones = int(arguments[2])
    port_tcp = 5000
    port_udp = 5001

    server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket_tcp.bind((host, port_tcp))
    server_socket_udp.bind((host, port_udp))

    server_socket_tcp.listen(nConexiones)
    print(f"Servidor TCP escuchando en {host}:{port_tcp}")
    print(f"Servidor UDP escuchando en {host}:{port_udp}")

    while True:
        try:
            client_socket, client_address = server_socket_tcp.accept()
            print(f"Conexión TCP establecida con {client_address}")

            tcp_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, client_address))
            tcp_thread.start()

        except socket.error:
            handle_udp_client(server_socket_udp)

if __name__ == "__main__":
    main()
