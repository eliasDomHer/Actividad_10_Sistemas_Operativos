import socket
import sys

def main():
    arguments = sys.argv
    if len(arguments) != 2:
        print(f"Uso: python clienteUDP.py <host>")
        exit(1)

    host = arguments[1]
    port_udp = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        destinatario = input("Ingrese el nombre del destinatario (o 'exit' para salir): ")
        if destinatario.lower() == 'exit':
            break

        message = input("Ingrese un mensaje: ")
        client_socket.sendto(f"{destinatario}:{message}".encode('utf-8'), (host, port_udp))

        # Esperar la respuesta del servidor
        try:
            response, server_address = client_socket.recvfrom(1024)
            print(f"Respuesta del servidor UDP: {response.decode('utf-8')}")
        except ConnectionResetError:
            print("Error: La conexión con el servidor UDP fue cerrada de forma inesperada.")

    # Cerrar la conexión UDP
    client_socket.close()

if __name__ == "__main__":
    main()
