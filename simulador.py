class Simulador:
    def __init__(self):
        self.comunidad = None
        self.results = {}

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad

    def run(self, pasos):
        for paso in range(pasos):
            self.comunidad.step()
            self.results[paso] = {
                'infected': self.comunidad.num_infectados,
                'recovered': self.comunidad.recuperados,
                'dead': self.comunidad.muertos,
                'population': (self.comunidad.num_ciudadanos - self.comunidad.muertos)
            }

    def get_results(self):
        return self.results
