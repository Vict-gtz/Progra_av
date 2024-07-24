import numpy as np
import random
import pandas as pd
from ciudadano import Ciudadano
from enfermedad import Enfermedad

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        # Inicio de los parámetros de la comunidad
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.num_infectados = num_infectados

        self.susceptibles = num_ciudadanos - num_infectados
        self.recuperados = 0
        self.muertos = 0
        self.poblacion = []
        self.results_df = pd.DataFrame()

    def personas_comunidad(self):
        # Crear y almacenar información de la población
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
        # Inicializar el estado de enfermedad de cada persona
        indices_infectados = np.random.choice(results_df.index, size=num_infectados, replace=False)
        results_df['enfermedad'] = False
        results_df.loc[indices_infectados, 'enfermedad'] = True

        # Asignar familias basadas en el apellido
        results_df['familia'] = results_df['apellido']
        grouped_df = results_df.groupby('familia')

        # Actualizar el DataFrame paso a paso
        self.update_infectados_por_familia(grouped_df)
        self.update_infectados_por_comunidad(results_df)
        
        return results_df

    def update_infectados_por_familia(self, grouped_df):
        # Actualizar infecciones basadas en contagio familiar
        for nombre_familia, grupo in grouped_df:
            infectados_familia = grupo[grupo['enfermedad'] == True].index.tolist()
            no_infectados_familia = grupo[grupo['enfermedad'] == False].index.tolist()

            if not infectados_familia:
                continue  # Si no hay infectados en la familia, no hay contagio

            probabilidad_familiar = self.enfermedad.prob_familiar

            for idx in no_infectados_familia:
                # Revisar el contagio con la probabilidad de contagio familiar
                if np.random.rand() < probabilidad_familiar:
                    self.results_df.at[idx, 'enfermedad'] = True

    def update_infectados_por_comunidad(self, results_df):
        # Obtenemos el número total de infectados
        infectados_comunidad = results_df[results_df['enfermedad'] == True].index.tolist()
        
        # Obtenemos el número total de no infectados
        no_infectados_comunidad = results_df[results_df['enfermedad'] == False].index.tolist()
        
        # Contamos el número de nuevos infectados por familia
        num_nuevos_infectados_familia = self.results_df['enfermedad'].sum()
        
        # Calculamos el número de nuevos infectados en la comunidad (total deseado)
        nuevos_infectados_totales = self.calcular_nuevos_infectados()
        
        # Calculamos cuántos infectados faltan después de considerar los infectados en familia
        nuevos_infectados_restantes = nuevos_infectados_totales - num_nuevos_infectados_familia
        
        # Si no hay suficientes personas para infectar, ajustamos el número
        if nuevos_infectados_restantes <= 0:
            return
        
        # Si no hay suficientes personas no infectadas, usamos todas las disponibles
        if len(no_infectados_comunidad) < nuevos_infectados_restantes:
            nuevos_infectados_restantes = len(no_infectados_comunidad)
        
        # Elegimos aleatoriamente entre los no infectados restantes
        indices_a_infectar = np.random.choice(no_infectados_comunidad, size=nuevos_infectados_restantes, replace=False)
        
        # Actualizamos el DataFrame
        self.results_df.loc[indices_a_infectar, 'enfermedad'] = True

    def actualizar_infectados(self, nuevos_infectados):
        # Filtra el DataFrame para obtener solo aquellos que no están infectados
        no_infectados_df = self.results_df[self.results_df['enfermedad'] == False]
        
        # Si no hay suficientes personas no infectadas, usa todas las disponibles
        if len(no_infectados_df) < nuevos_infectados:
            nuevos_infectados = len(no_infectados_df)
        
        # Selecciona aleatoriamente los nuevos infectados
        indices_a_infectar = np.random.choice(no_infectados_df.index, size=nuevos_infectados, replace=False)
        
        # Actualiza el DataFrame
        self.results_df.loc[indices_a_infectar, 'enfermedad'] = True

    def csv_crear(self, results_df):
        # Crear un archivo CSV con los datos de la comunidad
        results_df.drop(columns=['comunidad'], inplace=True)
        results_df.to_csv("ciudadanos_comunidad.csv", index=False)
        print(f"Personas de la comunidad fueron guardadas en ciudadanos_comunidad.csv")

    def get_dataframe(self):
        # Obtener el DataFrame de la comunidad
        comunidad = []
        for i in range(self.num_ciudadanos):
            persona = Ciudadano.crear_persona(i + 2000000, 1)
            comunidad.append(persona.__dict__)
        
        results_df = pd.DataFrame(comunidad)
        results_df = self.dataframe_info(results_df, self.num_infectados)
        return results_df

    def step(self):
        # Actualizar el estado de la comunidad en cada paso del tiempo
        nuevos_infectados = self.calcular_nuevos_infectados()
        nuevos_recuperados = self.calcular_nuevos_recuperados()
        
        self.actualizar_infectados(nuevos_infectados)
        
        self.num_infectados += nuevos_infectados - nuevos_recuperados
        self.recuperados += nuevos_recuperados
        self.susceptibles = max(self.num_ciudadanos - self.num_infectados - self.recuperados, 0)

    def calcular_nuevos_infectados(self):
        # Calcular el número de nuevos infectados basado en la probabilidad de infección
        nuevos_infectados = (self.enfermedad.infeccion_probable * self.num_infectados * self.susceptibles) / self.num_ciudadanos
        return int(nuevos_infectados)

    def calcular_nuevos_recuperados(self):
        # Calcular el número de nuevos recuperados basado en la tasa de recuperación
        nuevos_recuperados = int(self.enfermedad.tasa_recuperacion * self.num_infectados)
        return min(nuevos_recuperados, self.num_infectados)
