import socket
import select

# Cabecera, IP y puertos de conexión.

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 2598

# Se crea el socket y se setea la ip y puerto.

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s_socket.bind((IP, PORT))
s_socket.listen()

# Lista y diccionario de los datos recibidos.

lista_sockets = [s_socket]
clientes = {}

# Método para recibir mensajes, recibe como parámetro el socket cliente.

def recibir_mensajes(c_socket):

    try:

        # Crea un header dependiendo de la longitud del mensaje.

        msj_header = c_socket.recv(HEADER_LENGTH)

        # Si la longitud es 0 regresa un false.

        if not len(msj_header):

            return False
        
        # Decodifica el mensaje y lo muestra.

        msj_lenght = int(msj_header.decode('utf-8').strip())
        return{"header": msj_header, "data": c_socket.recv(msj_lenght)}

    except:
        
        pass

# Bucle infinito que corre el programa.

while True:

    # Variables para almacenar los datos recibidos.

    leer_sockets, _, exception_sockets = select.select(lista_sockets, [], lista_sockets)

    # Se recorre los datos recibidos.

    for socket_notificado in leer_sockets:

        # Si el socket que llegó equivale a lo que tiene el objeto acepta el mensaje y lo muestra.

        if socket_notificado == s_socket:

            c_socket, cliente_direccion = s_socket.accept()

            user = recibir_mensajes(c_socket)

            if user is False:

                continue

            lista_sockets.append(c_socket)
            clientes[c_socket] = user

            # Muestra la conexión recibida.

            print(f"Nueva conexión aceptada de {cliente_direccion[0]}:{cliente_direccion[1]} usuario: {user['data']. decode('utf-8')}")

        else:

            mensaje = recibir_mensajes(socket_notificado)

            if mensaje is False:

                # Muestra que la conexión de un usuario terminó.

                print(f"Conexión terminada de {clientes[socket_notificado]['data'].decode('utf-8')}")
                lista_sockets.remove(socket_notificado)
                del clientes[socket_notificado]
                continue

            user = clientes[socket_notificado]

            # Muestra el mensaje recibido de un usuario.

            print(f"Mensaje recibido de {user ['data'].decode('utf-8')}:{mensaje['data'].decode('utf-8')}")

            for c_socket in clientes:

                if c_socket != socket_notificado:

                    c_socket.send(user['header']+ user['data'] + mensaje['header'] + mensaje['data'])

    # Limpia la tupla de los sockets en cola.

    for socket_notificado in exception_sockets:

        lista_sockets.remove(socket_notificado)
        del clientes[socket_notificado]