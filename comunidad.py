class Comunidad:
    def _init_(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica):
        self.num_ciudadanos = num_ciudadanos
        self.promedio_conexion_fisica = promedio_conexion_fisica
        self.enfermedad = enfermedad
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.ciudadanos = self.crear_ciudadanos(num_ciudadanos)
        self.infectar_ciudadanos(num_infectados)

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