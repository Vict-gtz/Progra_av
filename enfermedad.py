class Enfermedad:
    def __init__(self, infeccion_probable, promedio_pasos): #prob_familiar, prob_comunidad
        self.infeccion_probable = infeccion_probable #probabilidad de infectarse
        self.promedio_pasos = promedio_pasos #promedio de pasos antes de que se mueran
        self.enfermo = False #False = no enfermo
        self.pasos = 0 #pasos
        self.tasa_recuperacion = 0.05#verestoahora
        #self.prob_familiar = prob_familiar  # probabilidad de contagio en familia
        #self.prob_comunidad = prob_comunidad  # probabilidad de contagio en comunidad