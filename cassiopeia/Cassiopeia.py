# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import sys
import threading
import glob
import os
from gui.CassiopeiaUi import CassiopeiaUi
from PyQt5 import QtWidgets
from main import _startup
from setup_galaxy.setup_galaxy import SetupGalaxy

class Cassiopeia(QtWidgets.QDialog):
    def __init__(self):
        self.simulationthread = None
        self.file_path = os.path.join(os.path.dirname(__file__),'templates/*')
        self.list_of_files = self.get_files()
        self.latest_file = self.latest_file = max(self.list_of_files, key=os.path.getctime)
        self.cui = CassiopeiaUi(self,self.list_of_files)

    def run(self):
        self.cui.ui.show()

    def start_simulation_helper(self):
        #self.get_files()
        self.latest_file = self.latest_file = max(self.list_of_files, key=os.path.getctime)
        #_startup()
        _startup(self.latest_file, self.current_delta_t)

    def start_simulation(self,delta_t):
        self.current_delta_t = delta_t
        if self.simulationthread is None:
            print("Start the simulation")
            self.simulationthread = threading.Thread(target=self.start_simulation_helper)
            self.simulationthread.start()
        else:
            print("The simulation has already been started")

    def stop_simulation(self):
        if self.simulationthread is None:
            print("There is no simulation running")
        else:
            print("Begin murder")
            self.simulationthread.do_run = False
            self.simulationthread.join(1)
            self.simulationthread = None
            print("Thread exit. Have a nice day.")

    def initialize_simulation(self, params):
        print("Generate Json with given parameters")
        print(params)
        init = SetupGalaxy(*params)
        init.setup()


    def get_files(self):
        return glob.glob(self.file_path)
        print(self.list_of_files)

def start_ui():
    app = QtWidgets.QApplication(sys.argv)
    cassiopeia = Cassiopeia()
    cassiopeia.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_ui()
