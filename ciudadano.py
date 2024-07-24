import pandas as pd
import numpy as np

class Ciudadano:
    def __init__(self, _id, nombre, apellido, comunidad):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = apellido
        self.comunidad = f"comunidad {comunidad}"
        self.enfermedad = False # no enfermo

    @staticmethod
    def obtener_nombre_aleatorio():
        file = 'nombres.csv'
        df = pd.read_csv(file, header=None, names=['nombres'])
        nombres_apellidos = df['nombres'].str.split(' ', expand=True)
        nombre = nombres_apellidos[0].to_numpy()
        apellido = nombres_apellidos[1].to_numpy()
        
        nombre = np.random.choice(nombre)
        apellido = np.random.choice(apellido)
        return nombre, apellido

    @staticmethod
    def crear_persona(_id_, comunidad):
        nombres = Ciudadano.obtener_nombre_aleatorio()
        ciudadano = Ciudadano(_id=_id_, comunidad=comunidad, nombre=nombres[0], apellido=nombres[1])
        return ciudadano
