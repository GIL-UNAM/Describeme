# -*- coding: utf-8 -*-

#
#   Servidor
#   Enlazado al localhost por el puerto 8000 con protocolo TCP/IP
#   Espera una cadena del cliente, responde con: cadena + " desde Marte"
#

import socket
import threading
import sys
import queue
from datetime import date
from defineme_esp import diccionario_nap, ConstruyeGrafos
from defineme_eng import diccionario_limitado_eng, florida_graph
from bitacora import Bitacora
from bitacora import Evento


# Función que concatena la oración y la frase " desde Marte."
def obtieneIP():
    # Regresa la dirección IP del equipo
    return str(socket.gethostbyname(socket.gethostname()))



def procesaPeticion(conexion, direccion):
    try:
        # Recibe una oración del cliente y el idioma a utilizar
        informacion = conexion.recv(8192).decode()
        informacion = informacion.split('|')
        oracion = informacion[0]
        idioma = informacion[1]

        # Si la oración contiene algo
        if oracion:

            # Notifica de la nueva petición
            print(f"El cliente {direccion} ha enviado una oración.")
            print(f"Oración recibida: '{oracion}'.")
            print(f"Idioma: {idioma}")

            # Prepara una respuesta y la envía
            if idioma == "ESP":
                terminos = diccionario_nap(oracion, grafo_esp)
            else:
                terminos = diccionario_limitado_eng(oracion, grafo_eng)
            conexion.send(terminos.encode())

            bloquea.acquire()
            try:    
                # Escribe en registros.tsv el registro de la petición
                Bitacora.evento(Evento.peticion, str(direccion[0]), oracion, terminos)
            finally:
                # Termina el bloqueo
                bloquea.release()
                
            # Cierra el socket
            print(f"Petición completada, conexión terminada con {direccion}.\n")
            conexion.close()
    except:
        pass



def aceptaPeticion():

    while True:
        # Espera una petición del usuario
        conexion, direccion = mi_socket.accept()
        print(f"\nNueva conexion extablecida con: {direccion}")
        
        # Crea un hilo para procesar la petición
        procesa = threading.Thread(target=procesaPeticion, args=(conexion, direccion,))
        procesa.daemon = False
        procesa.start()



# Crea el grafo en español
print("Creando el grafo en español...")
grafos = ConstruyeGrafos()
grafo_esp = grafos[2]
print("Se creó el grafo exitosamente.")

# Crea el grafo en inglés
print("Creando el grafo en inglés...")
grafo_eng = florida_graph()
print("Se creó el grafo exitosamente.")

# Variable de control
output = "salir"

# Crea un objeto socket con valores default
mi_socket = socket.socket()

# Establece conexión por el puerto 8000
mi_socket.bind(('localhost', 5050))

# Establece cantidad de peticiones en cola manejables
mi_socket.listen(1000)

# Variable para bloquear el acceso a recursos compartidos entre hilos
bloquea = threading.Lock()

# Crea hilo para esperar y aceptar peticiones
acepta = threading.Thread(target=aceptaPeticion)
acepta.daemon = False
acepta.start()

# Guarda el inició del servidor en el archivo test.tsv
Bitacora.evento(Evento.inicio_servidor, obtieneIP())

# El hilo principal espera a que termine la ejecución del servidor
if __name__ == '__main__':
  while True:
    try:
          salida = input()
          if salida.upper() == output.upper():
              # Termina la conexión
              mi_socket.close()

              # Guarda el fin del servidor en el archivo registros.tsv
              Bitacora.evento(Evento.fin_servidor, obtieneIP())

              # Sale del ciclo
              break
          else:
              pass
    except EOFError:
          pass
