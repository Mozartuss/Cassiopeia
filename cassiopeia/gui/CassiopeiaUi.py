# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtGui, uic, QtCore

class CassiopeiaUi(QtWidgets.QDialog):
    # constructor
    def __init__(self, api):
        print("ui.__init__")
        QtWidgets.QDialog.__init__(self)
        # load and show the user interface created with the designer.
        self.entrypoint = api
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__),'CassiopeiaUI.ui'))
        self.set_connections()

    def set_connections(self):
        print("ui.set_connections")
        self.ui.btnStart.clicked.connect(self.on_start)
        self.ui.btnStop.clicked.connect(self.on_stop)
        self.ui.btnInitialize.clicked.connect(self.on_initialize)
        #self.ui.btnPause.clicked.connect(self.pause_simulation)
        #self.ui.btnInitialize.clicked.connect(self.initialize_simulation)

    def on_initialize(self):
        print("write to json")
        self.entrypoint.initialize_simulation()

    def on_start(self):
        print("connect button pressed")
        self.entrypoint.start_simulation()

    def on_stop(self):
        print("disconnect button pressed")
        self.entrypoint.stop_simulation()

    def close(self):
        print("ui.close")
        #self.ui.close()
        #start_ui()
        pass

    def initialize_simulation(self):
        print("ui.initialize_simulation")
        settings['p_mass_min'] = self.ui.hsPlanetMinMass.value()
        settings['p_mass_max'] = self.ui.hsPlanetMaxMass.value()
        settings['p_rad_min'] = self.ui.hsPlanetMinRad.value()

    def start_simulation(self):
        print("ui.start_simulation")
        #main._startup()
        #start()
        #self.ui.close()
        #CassiopeiaCoreClasse.Start()

    def stop_simulation(self):
        print("ui.stop_simulation")
        self.ui.close()
        #CassiopeiaCoreClass.Stop()

    def pause_simulation(self):
        print("ui.pause_simulation")
        self.ui.close()
        #CassiopeiaCoreClass.Pause()
