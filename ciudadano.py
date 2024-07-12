class Ciudadano:
    def __init__(self, id, nombre, apellido, familia, comunidad, enfermedad):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = familia
        self.comunidad = comunidad
        self.enfermedad = enfermedad
        self.estado = True  # True si vivo o muerto