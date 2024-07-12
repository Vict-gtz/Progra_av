import gi
import time
import threading
import pandas as pd
import sys
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Simulador de Epidemia")
        self.set_default_size(800, 600)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.vbox)

        self.label = Gtk.Label(label="Configuración de la Simulación")
        self.vbox.append(self.label)

        self.button_start = Gtk.Button(label="Iniciar Simulación")
        self.button_start.connect("clicked", self.on_start_simulation)
        self.vbox.append(self.button_start)

        self.community_labels = []
        for i in range(4):
            label = Gtk.Label()
            self.vbox.append(label)
            self.community_labels.append(label)

        self.simuladores = [Simulador() for _ in range(4)]
        self.csv_data = [[] for _ in range(4)]
        self.current_step = 0

    def save_results_to_csv(self, results, index):
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
        results_df.to_csv(f"simulacion_comunidad_{index+1}.csv", index=False)
        print(f"Resultados guardados en simulacion_comunidad_{index+1}.csv")

    def on_start_simulation(self, widget):
        self.comunidades = []
        for i in range(4):
            covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)
            comunidad = Comunidad(num_ciudadanos=20000, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=10, probabilidad_conexion_fisica=0.8)
            self.simuladores[i].set_comunidad(comunidad)
            self.simuladores[i].run(pasos=45)
            self.save_results_to_csv(self.simuladores[i].get_results(), i)
            self.comunidades.append(comunidad)
        
        self.read_csv_data()
        self.start_update_loop()

    def read_csv_data(self):
        for i in range(4):
            df = pd.read_csv(f"simulacion_comunidad_{i+1}.csv")
            self.csv_data[i] = df.to_dict('records')

    def update_labels(self):
        if self.current_step < len(self.csv_data[0]):
            for i, label in enumerate(self.community_labels):
                data = self.csv_data[i][self.current_step]
                text = f"Comunidad {i+1} - Día: {data['Días']}, Infectados: {data['Infectados']}, Recuperados: {data['Recuperados']}, Muertos: {data['Muertos']}, Población Total: {data['Población Total']}"
                label.set_text(text)
            self.current_step += 1
        else:
            self.current_step = 0

    def start_update_loop(self):
        def update_loop():
            while True:
                time.sleep(1)
                GLib.idle_add(self.update_labels)

        threading.Thread(target=update_loop, daemon=True).start()

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
