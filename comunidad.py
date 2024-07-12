import random
from ciudadano import Ciudadano

class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.ciudadanos = self.crear_ciudadanos(num_ciudadanos)
        self.infectar_ciudadanos(num_infectados)
        self.num_infectados = num_infectados

    def crear_ciudadanos(self, num):
        ciudadanos = []
        for i in range(num):
            ciudadano = Ciudadano(i, f"Nombre_{i}", f"Apellido_{i}", self, f"Familia_{i // 4}")
            ciudadanos.append(ciudadano)
        return ciudadanos

    def infectar_ciudadanos(self, num_infectados):
        infectados = random.sample(self.ciudadanos, num_infectados)
        for ciudadano in infectados:
            ciudadano.infectar(self.enfermedad)

    def actualizar_estado(self):
        self.num_infectados = sum(1 for c in self.ciudadanos if c.enfermedad)
        self.num_recuperados = sum(1 for c in self.ciudadanos if c.estado == 'recuperado')
        self.num_muertos = sum(1 for c in self.ciudadanos if c.estado == 'muerto')
