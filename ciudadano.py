import random

class Ciudadano:
    def _init_(self, id, nombre, apellido, comunidad, familia, enfermedad=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.comunidad = comunidad
        self.familia = familia
        self.enfermedad = enfermedad
        self.estado = True  # True indica que el ciudadano está sano o muerto (no infectado)

    def infectar(self, enfermedad):
        if self.enfermedad is None:
            self.enfermedad = enfermedad
            self.contador = 0

    def paso(self):
        if self.enfermedad is not None:
            self.contador += 1
            if self.contador > self.enfermedad.promedio_pasos:
                self.enfermedad = None