import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def _init_(self):
        super()._init_(title="Simulación de Enfermedades Infecciosas")
        self.set_border_width(10)

        grid = Gtk.Grid()
        self.add(grid)

        self.label = Gtk.Label(label="Simulación de Enfermedades Infecciosas")
        grid.attach(self.label, 0, 0, 1, 1)

        self.button = Gtk.Button(label="Iniciar Simulación")
        self.button.connect("clicked", self.on_button_clicked)
        grid.attach(self.button, 0, 1, 1, 1)

    def on_button_clicked(self, widget):
        covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)
        talca = Comunidad(num_ciudadanos=20000, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=10, probabilidad_conexion_fisica=0.8)
        sim = Simulador()
        sim.set_comunidad(talca)
        sim.run(pasos=45)

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()