import csv
import random

class Simulador:
    def __init__(self):
        self.comunidad = None
        self.results = {}

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def run(self, pasos):
        for paso in range(pasos):
            self.simular_paso()
            self.actualizar_estado()
            self.generar_reporte_csv(paso)
            self.imprimir_estado(paso)
            self.results[paso] = {
                'infected': self.comunidad.num_infectados,
                'recovered': self.comunidad.num_recuperados,
                'dead': self.comunidad.num_muertos
            }

    def simular_paso(self):
        for ciudadano in self.comunidad.ciudadanos:
            if ciudadano.enfermedad is not None:
                for otro in random.sample(self.comunidad.ciudadanos, self.comunidad.promedio_conexion_fisica):
                    if otro.enfermedad is None and random.random() < self.comunidad.enfermedad.infeccion_probable:
                        otro.infectar(self.comunidad.enfermedad)
            ciudadano.paso()

    def actualizar_estado(self):
        self.comunidad.num_infectados = sum(1 for c in self.comunidad.ciudadanos if c.enfermedad is not None)
        self.comunidad.num_recuperados = sum(1 for c in self.comunidad.ciudadanos if c.estado == 'recuperado')
        self.comunidad.num_muertos = sum(1 for c in self.comunidad.ciudadanos if c.estado == 'muerto')

    def generar_reporte_csv(self, paso):
        with open(f'reporte_paso_{paso}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nombre', 'Apellido', 'Familia', 'Enfermedad', 'Estado'])
            for ciudadano in self.comunidad.ciudadanos:
                writer.writerow([
                    ciudadano._id, ciudadano.nombre, ciudadano.apellido,
                    ciudadano.familia, ciudadano.enfermedad is not None,
                    ciudadano.estado
                ])

    def imprimir_estado(self, paso):
        infectados = sum(1 for c in self.comunidad.ciudadanos if c.enfermedad is not None)
        total = len(self.comunidad.ciudadanos)
        print(f"Paso {paso}: Infectados: {infectados}/{total}")
