import pandas as pd
import random
import numpy as np

class Ciudadano:
    def __init__(self, _id, nombre, apellido, familia, comunidad):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = familia # identificador (apellido)
        self.comunidad = comunidad
        self.enfermedad = False # no enfermo
        self.estado = True # vivo

    
    def obtener_nombre_aleatorio():
        file = 'nombres.csv'
        df = pd.read_csv(file, header=None, names=['nombres'])
        nombres_apellidos = df['nombres'].str.split(' ', expand=True)
        nombre = nombres_apellidos[0].to_numpy()
        apellido = nombres_apellidos[1].to_numpy()
        
        nombre = np.random.choice(nombre)
        apellido = np.random.choice(apellido)
        return nombre, apellido

#crear ciudadano
nombres = Ciudadano.obtener_nombre_aleatorio()
ciudadano = Ciudadano(_id=1, comunidad="Comunidad1", nombre=nombres[0], apellido=nombres[1], familia=nombres[1])

print(f"Ciudadano creado: {ciudadano.nombre} {ciudadano.apellido}")