class Enfermedad:
    def __init__(self, infeccion_probable, promedio_pasos):
        self.tasa_transmision = infeccion_probable
        self.promedio_pasos = promedio_pasos
        self.tasa_recuperacion = 1 / promedio_pasos
