import gi
import numpy as np
import pandas as pd
import random
import sys
import threading
import time

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Simulador SIR")
        self.set_default_size(750, 500)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.vbox)

        self.button_start = Gtk.Button(label="Iniciar Simulación")
        self.button_start.connect("clicked", self.on_start_simulation)
        self.vbox.append(self.button_start)

        # Labels para mostrar la información de la simulación
        self.info_label = Gtk.Label()
        self.vbox.append(self.info_label)

        # Label para mostrar el DataFrame de ciudadanos
        self.df_label = Gtk.Label()
        self.vbox.append(self.df_label)

        self.simulador = Simulador()
        self.keep_updating = False  # para parar el loop

    def save_results_to_csv(self, results):
        data = []
        for step, result in results.items():
            data.append({
                'Días': step,
                'Infectados': result['infected'],
                'Recuperados': result['recovered'],
                'Muertos': result['dead'],
                'Población Total': result['population']
            })
        results_df = pd.DataFrame(data)
        results_df.to_csv("simulacion_comunidad.csv", index=False)
        print(f"Resultados guardados en simulacion_comunidad.csv")

    def on_start_simulation(self, widget):
        enfermedad = Enfermedad(infeccion_probable=0.3, promedio_pasos=4, prob_familiar=0.5, prob_comunidad=0.1)
        comunidad = Comunidad(
            num_ciudadanos=random.randint(1200, 2000),
            promedio_conexion_fisica=8,
            enfermedad=enfermedad,
            num_infectados=random.randint(60, 230),
            probabilidad_conexion_fisica=0.8
        )
        comunidad.personas_comunidad()
        self.simulador.set_comunidad(comunidad)
        self.simulador.run(pasos=41)
        self.save_results_to_csv(self.simulador.get_results())

        self.df_personas = comunidad.poblacion_df
        self.display_dataframe(self.df_personas)

        self.start_update_loop()

    def display_dataframe(self, df):
        df_str = df.to_string(max_rows=20)  
        self.df_label.set_text(df_str)

    def update_labels(self):
        if self.current_step < len(self.csv_data):
            data = self.csv_data[self.current_step]
            info_text = (f"Día: {data['Días']}, Infectados: {data['Infectados']}, "
                         f"Recuperados: {data['Recuperados']}, Muertos: {data['Muertos']}, "
                         f"Población Total: {data['Población Total']}")
            self.info_label.set_text(info_text)
            self.display_dataframe(self.df_personas)
            self.current_step += 1
        else:
            self.keep_updating = False  # Detener el loop cuando ya se lean todos los datos

    def start_update_loop(self):
        self.current_step = 0
        self.read_csv_data()
        self.keep_updating = True

        def update_loop():
            while self.keep_updating:
                time.sleep(1)
                GLib.idle_add(self.update_labels)

        threading.Thread(target=update_loop, daemon=True).start()

    def read_csv_data(self):
        df = pd.read_csv("simulacion_comunidad.csv")
        self.csv_data = df.to_dict('records')  # df a dic

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

app = MyApp()
app.run(sys.argv)