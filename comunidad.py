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
        self.num_infectados = num_infectados#########CAMBIAMUCHO

        self.susceptibles = num_ciudadanos - num_infectados
        self.recuperados = 0
        self.muertos = 0
        self.poblacion = []

        # DataFrame para el estado de salud de la población
        self.results_df = pd.DataFrame()

    def personas_comunidad(self):
        comunidad = []
        for i in range(self.num_ciudadanos):
            persona = Ciudadano.crear_persona(i + 2000000, 1)
            comunidad.append(persona.__dict__)

        self.poblacion = comunidad
        self.results_df = pd.DataFrame(comunidad)
        self.results_df = self.dataframe_info(self.results_df, self.num_infectados)
        self.csv_crear(self.results_df)
        self.poblacion_df = self.results_df 

    def dataframe_info(self, results_df, num_infectados):
        indices_infectados = np.random.choice(results_df.index, size=num_infectados, replace=False)
        
        results_df['enfermedad'] = False
        results_df.loc[indices_infectados, 'enfermedad'] = True

        results_df['familia'] = results_df['apellido']
        grouped_df = results_df.groupby('familia')

        # Actualizar el DataFrame paso a paso
        self.update_infectados_por_familia(grouped_df)
        self.update_infectados_por_comunidad(results_df)
        
        return results_df

    def update_infectados_por_familia(self, grouped_df):
        for nombre_familia, grupo in grouped_df:
            infectados_familia = grupo[grupo['enfermedad'] == True].index.tolist()
            no_infectados_familia = grupo[grupo['enfermedad'] == False].index.tolist()

            for idx in no_infectados_familia:
                # Revisar el contagio con la probabilidad de contagio familiar
                if np.random.rand() < self.enfermedad.prob_familiar * len(infectados_familia) / len(grupo):
                    self.results_df.at[idx, 'enfermedad'] = True


    def update_infectados_por_comunidad(self, results_df):
        infectados_comunidad = results_df[results_df['enfermedad'] == True].index.tolist()
        no_infectados_comunidad = results_df[results_df['enfermedad'] == False].index.tolist()

        for idx in no_infectados_comunidad:
            # Revisar el contagio con la probabilidad de contagio comunitario
            if np.random.rand() < self.enfermedad.prob_comunidad * len(infectados_comunidad) / len(results_df):
                results_df.at[idx, 'enfermedad'] = True



    def csv_crear(self, results_df):
        results_df.drop(columns=['comunidad'], inplace=True)
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
        
        self.num_infectados += new_infectados - new_recuperados - new_muertos
        self.recuperados += new_recuperados
        self.muertos += new_muertos
        
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
