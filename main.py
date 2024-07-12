import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
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

        self.text_view = Gtk.TextView()
        self.vbox.append(self.text_view)

        self.simulador = Simulador()

    def save_results_to_csv(self, results):
        data = []
        for step, result in results.items():
            data.append({
                'Días': step,
                'Infectados': result['infected'],
                'Recuperados': result['recovered'],
                'Muertos': result['dead']
            })
        results_df = pd.DataFrame(data)
        results_df.to_csv("simulacion.csv", index=False)
        print("Resultados guardados en simulacion.csv")

    def on_start_simulation(self, widget):
        covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)
        talca = Comunidad(num_ciudadanos=20000, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=10, probabilidad_conexion_fisica=0.8)
        self.simulador.set_comunidad(talca)
        self.simulador.run(pasos=45)
        
        self.show_results()

    def show_results(self):
        self.save_results_to_csv(self.simulador.get_results())
        buffer = self.text_view.get_buffer()
        buffer.set_text("Simulación completada. Los resultados han sido guardados en resultados_simulacion.csv.")

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
