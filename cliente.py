import socket
import select
import errno
import sys


# Cabecera, IP y puerto del socket.

HEADER_LENGTH = 10
IP = "127.0.0.1" 
PORT = 2598

# Input para ingresar el usuario.

my_user = input("Usuario: ")

# Se crea el socket y establece la conexión al servidor.

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect((IP, PORT))

# Este método desbloquea los sockets para poder enviar múltiples mensajes.

c_socket.setblocking(False)

# Envía el usuario y lo códifica.

username = my_user.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
c_socket.send(username_header + username)

# Bucle infinito que corre el programa.

while True:

    # Muestra el usuario conectado y donde ingresará el mensaje.

    mensaje= input(f"{my_user} -> ")

    # Si el mensaje no está vació se envía.

    if mensaje:

        mensaje = mensaje.encode('utf-8')
        message_header = f"{len(mensaje):< {HEADER_LENGTH}}".encode('utf-8')
        c_socket.send(message_header + mensaje)

    try:
        while True:

            # Cosas recibidas.
            username_header = c_socket.recv(HEADER_LENGTH)

            # Si la cabecera del usuario está vacía termina la conexión.

            if not len(username_header):

                print("Conexión cerrada por el servidor")
                sys.exit()

            # Y si no, códifica la cabecera y lo envía al servidor.    

            username_length = int(username_header.decode('utf-8').strip())
            username = c_socket.recv(username_length). decode('utf-8')

            # Se codifica y se envía la cabecera del mensaje.

            message_header = c_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message= c_socket.recv(message_length).decode('utf-8')

            # Mustra el usuario y el mensaje escrito.

            print(f"{username} > {message}")

    # Control de excepciones.        

    except IOError as e:

        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:

            print("Error de lectura", str(e))
            sys.exit()

        continue

    except Exception as e:
        
        print('Error general', str(e))
        sys.exit()
        pass
