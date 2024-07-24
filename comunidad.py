import numpy as np
import random
import pandas as pd
from ciudadano import Ciudadano
from enfermedad import Enfermedad

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.num_infectados = num_infectados
        
        self.susceptibles = num_ciudadanos - num_infectados
        self.recuperados = 0
        self.muertos = 0
        self.poblacion = []

    def personas_comunidad(self):
        comunidad = []
        for i in range(self.num_ciudadanos):
            persona = Ciudadano.crear_persona(i + 2000000, 1)
            comunidad.append(persona.__dict__)

        self.poblacion = comunidad

        comunidad_personas = "comunidad_1"#matar esto dsp
        results_df = pd.DataFrame(comunidad)
        results_df = self.dataframe_info(results_df, self.num_infectados)
        self.csv_crear(results_df, comunidad_personas)
        self.poblacion_df = results_df 

    def dataframe_info(self, results_df, num_infectados):
        # Seleccionar aleatoriamente a los infectados
        indices_infectados = np.random.choice(results_df.index, size=num_infectados, replace=False)
        
        # Marcar los ciudadanos seleccionados como infectados
        results_df['enfermedad'] = False
        results_df.loc[indices_infectados, 'enfermedad'] = True

        # Agrupación por familia
        results_df['familia'] = results_df['apellido']
        grouped_df = results_df.groupby('familia')

        for nombre_familia, grupo in grouped_df:
            if grupo['enfermedad'].any():
                for index, row in grupo.iterrows():
                    if row['enfermedad']:
                        # Infectar a otros miembros de la misma familia
                        if np.random.rand() < self.enfermedad.infeccion_probable:
                            results_df.at[index, 'enfermedad'] = True
        return results_df

    def csv_crear(self, results_df, comunidad_personas):
        results_df.to_csv("ciudadanos_comunidad.csv", index=False)
        print(f"Personas de la comunidad fueron guardadas en ciudadanos_comunidad.csv")

    def get_dataframe(self):
        comunidad = []
        for i in range(self.num_ciudadanos):
            persona = Ciudadano.crear_persona(i + 2000000, 1)
            comunidad.append(persona.__dict__)
        
        results_df = pd.DataFrame(comunidad)
        results_df = self.dataframe_info(results_df, self.num_infectados)
        return results_df
    
    def step(self):
        new_infectados = self.calcular_nuevos_infectados()
        new_recuperados = self.calcular_nuevos_recuperados()
        new_muertos = self.calcular_nuevos_muertos()
        
        # Actualiza las cifras de infectados, recuperados y muertos
        self.num_infectados += new_infectados - new_recuperados - new_muertos
        self.recuperados += new_recuperados
        self.muertos += new_muertos
        
        # Asegúrate de no tener valores negativos
        self.num_infectados = max(self.num_infectados, 0)
        self.recuperados = max(self.recuperados, 0)
        self.muertos = max(self.muertos, 0)
        
        self.susceptibles = self.num_ciudadanos - self.num_infectados - self.recuperados - self.muertos

        if self.susceptibles < 0:
            self.susceptibles = 0
    
    def calcular_nuevos_infectados(self):
        t_s_i = (self.enfermedad.infeccion_probable * self.susceptibles * self.num_infectados)
        rec_inf = (self.enfermedad.tasa_recuperacion * self.num_infectados)
        posibles_infectados = max(int(round(t_s_i - rec_inf)), 0)
        
        nuevas_infecciones = (np.sum(np.random.rand(int(posibles_infectados)) < self.probabilidad_conexion_fisica))
        return min(nuevas_infecciones, self.susceptibles)
    
    def calcular_nuevos_recuperados(self):
        nuevos_recuperados = int(round(self.enfermedad.tasa_recuperacion * self.num_infectados))
        return min(nuevos_recuperados, self.num_infectados)
    
    def calcular_nuevos_muertos(self):
        tasa_mortalidad = 0.02
        nuevos_muertos = int(round(tasa_mortalidad * self.num_infectados))
        return min(nuevos_muertos, self.num_infectados)
