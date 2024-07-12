class Ciudadano:
    def __init__(self, _id, nombre, apellido, familia, comunidad):
        self._id = _id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = familia
        self.comunidad = comunidad
        self.enfermedad = None
        self.estado = 'sano' # 'sano', 'infectado', 'recuperado', 'muerto'

    def infectar(self, enfermedad):
        self.enfermedad = enfermedad
        self.estado = 'infectado'
