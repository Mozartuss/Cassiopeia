# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import sys
import threading
from gui.CassiopeiaUi import CassiopeiaUi
from PyQt5 import QtWidgets
from main import _startup

class Cassiopeia(QtWidgets.QDialog):
    def __init__(self):
        self.cui = CassiopeiaUi(self)
        self.simulationthread = None

    def run(self):
        self.cui.ui.show()

    def start_simulation_helper(self):
        _startup("random_planets_x18.json", 60 * 60)

    def start_simulation(self):
        if self.simulationthread is None:
            print("Start the simulation")
            self.simulationthread = threading.Thread(target=self.start_simulation_helper)
            self.simulationthread.start()
        else:
            print("The simulation was already started")

    def stop_simulation(self):
        if self.simulationthread is None:
            print("There is no simulation running")
        else:
            print("Begin murder")
            self.simulationthread.do_run = False
            self.simulationthread.join(5)
            self.simulationthread = None
            print("Thread exit. Have a nice day.")

    def initialize_simulation(self):
        print("Generate Json with given parameters")

def start_ui():
    app = QtWidgets.QApplication(sys.argv)
    cassiopeia = Cassiopeia()
    cassiopeia.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_ui()
