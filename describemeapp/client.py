#
#   Cliente
#   Contiene las funciones para crear un socket, enviar un 
#   mensaje al servidor y cerrar el socket.   
#

import socket

def creaSocket():
    # Crea un objeto socket con valores default
    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Inicia la conexión
    mi_socket.connect( ('localhost', 5050) )

    return mi_socket


def enviaMensaje(mi_socket, oracion, idioma):
    # Cadena de n términos
    terminos = ""

    # Concatena la oracion y el idioma separados por una coma
    informacion = oracion + '|' + idioma

    # Envía la informacion al servidor
    mi_socket.send(informacion.encode())

    # Recibe respuesta del demonio (buffer = 1024 Bytes)
    terminos = mi_socket.recv(8192).decode()
    terminos = terminos.split(',')
    terminos.pop(0)
    return terminos


def cierraSocket(mi_socket):
    # Cierra el socket
    mi_socket.close()
