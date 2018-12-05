import glob
import os
import sys
import threading

from PyQt5 import QtWidgets

from gui.cassiopeia_ui import CassiopeiaUi
from main import _startup
from setup_galaxy.setup_galaxy import SetupGalaxy


class Cassiopeia(QtWidgets.QDialog):
    def __init__(self):
        self.simulation_thread = None
        self.file_path = os.path.join(os.path.dirname(__file__), 'templates/*')
        self.list_of_files = self.get_files()
        self.cui = CassiopeiaUi(self, self.list_of_files)

    def run(self):
        self.cui.show()

    def start_simulation_helper(self, delta_t, path):
        _startup(path, delta_t)

    def start_simulation(self, delta_t, path=None):
        if path is None:
            current_path = max(self.get_files(), key=os.path.getctime)
        else:
            current_path = path

        if self.simulation_thread is None:
            print("Start the simulation")
            self.simulation_thread = threading.Thread(target=self.start_simulation_helper,
                                                      args=(delta_t, current_path))
            self.simulation_thread.start()
        else:
            print("The simulation has already been started", )

    def stop_simulation(self):
        if self.simulation_thread is None:
            print("WARNING: There is no simulation running")
        else:
            print("\n \nBegin murder")
            self.simulation_thread.do_run = False
            self.simulation_thread.join(1)
            self.simulation_thread = None
            print("Thread exit. Have a nice day.")

    def initialize_simulation(self, params):
        print("Generate Json with given parameters")
        init = SetupGalaxy(*params)
        init.setup()

    def get_files(self):
        return glob.glob(self.file_path)


def start_ui():
    app = QtWidgets.QApplication(sys.argv)
    cassiopeia = Cassiopeia()
    cassiopeia.run()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_ui()
