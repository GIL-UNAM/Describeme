import os
import enum
import threading
from datetime import date

# Define los eventos
@enum.unique
class Evento(enum.Enum):

    fin_servidor = 2
    inicio_servidor = 1
    peticion = 0


# Escribe eventos en la bitácora
class Bitacora():

    # Define nombre del archivo
    nombreArchivo = 'registros.tsv'

    # Escribe el registro en el archivo
    @staticmethod   # Define el método como método estático
    def escribeBitacora(registro, nombreArchivo):
        f = open(nombreArchivo, 'a')
        f.write(registro)
        f.close()

    # Registra un evento en la bitácora
    @classmethod
    def evento(cls, numeroEvento, direccionIP, *lista):
        # Registra una petición
        if numeroEvento == Evento.peticion:
            registro = str(date.today()) + '\t' + direccionIP + '\t' + lista[0] + '\t' + lista[1] + '\n'
            cls.escribeBitacora(registro, cls.nombreArchivo)

        # Registra el inicio del servidor
        elif numeroEvento == Evento.inicio_servidor:
            registro = str(date.today()) + "\t" + direccionIP + "\t\tSe inicio el servidor\n"
            cls.escribeBitacora(registro, cls.nombreArchivo)

        # Registra el fin del servidor
        elif numeroEvento == Evento.fin_servidor:
            registro = str(date.today()) + "\t" + direccionIP + "\t\tSe apago el servidor\n"
            cls.escribeBitacora(registro, cls.nombreArchivo)