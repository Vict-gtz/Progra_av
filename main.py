# main.py
import gi
import time
import threading
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador
import sys
import pandas as pd

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

        self.community_text_views = []
        for i in range(4):
            text_view = Gtk.TextView()
            self.vbox.append(text_view)
            self.community_text_views.append(text_view)

        self.simuladores = [Simulador() for _ in range(4)]

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

        self.update_text_views()
        self.start_update_loop()

    def update_text_views(self):
        for i, text_view in enumerate(self.community_text_views):
            buffer = text_view.get_buffer()
            comunidad = self.comunidades[i]
            text = f"Comunidad {i+1} - Población: {comunidad.num_ciudadanos}, Infectados: {comunidad.infectados}, Recuperados: {comunidad.recuperados}, Muertos: {comunidad.muertos}"
            buffer.set_text(text)

    def start_update_loop(self):
        def update_loop():
            while True:
                time.sleep(1)
                GLib.idle_add(self.update_text_views)

        threading.Thread(target=update_loop, daemon=True).start()

# Base del programa
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
