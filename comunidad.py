#Imports
import numpy as np
import random
import pandas as pd
from ciudadano import Ciudadano

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.num_infectados = num_infectados
        
        self.susceptibles = num_ciudadanos - num_infectados # Los que se pueden infectar
        self.recuperados = 0
        self.muertos = 0
    
    
    def personas_comunidad(self, miaucomunidad):
        comunidad = []
        for i in range(self.num_ciudadanos):
            persona = Ciudadano.crear_persona(i+2000000, miaucomunidad+1)
            comunidad.append(persona.__dict__)  # Convertir a dic para df
        comunidad_personas = persona.comunidad
        results_df = pd.DataFrame(comunidad)
        results_df.to_csv(f"ciudadanos_{persona.comunidad}.csv", index=False)
        print(f"Personas de la comunidad fueron guardadas en ciudadanos_{persona.comunidad}.csv")
    
    def step(self):
        new_infectados = self.calcular_nuevos_infectados()
        new_recuperados = self.calcular_nuevos_recuperados()
        new_muertos = self.calcular_nuevos_muertos()
        
        self.susceptibles -= new_infectados
        self.num_infectados += new_infectados - new_recuperados - new_muertos
        self.recuperados += new_recuperados
        self.muertos += new_muertos
        
        if self.num_infectados < 0:
            self.num_infectados = 0
        if self.susceptibles < 0:
            self.susceptibles = 0
    
    
    #SIR #CAMBIARESTO"""""""""dsp
    def calcular_nuevos_infectados(self):
        posibles_infectados = self.num_infectados * self.promedio_conexion_fisica
        nuevas_infecciones = np.sum(np.random.rand(int(posibles_infectados)) < self.probabilidad_conexion_fisica)
        return min(nuevas_infecciones, self.susceptibles)
    
    def calcular_nuevos_recuperados(self):
        nuevos_recuperados = int(round(self.enfermedad.tasa_recuperacion * self.num_infectados))
        return min(nuevos_recuperados, self.num_infectados)
    
    def calcular_nuevos_muertos(self):
        tasa_mortalidad = 0.02
        nuevos_muertos = int(round(tasa_mortalidad * self.num_infectados))
        return min(nuevos_muertos, self.num_infectados)

