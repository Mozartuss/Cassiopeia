# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtGui, uic, QtCore

class CassiopeiaUi(QtWidgets.QDialog):
    """
    Class which sets up the program's GUI.
    """
    # constructor
    def __init__(self, api, list_of_files):
        """
        Constructor
        :param api: Instance of Cassiopeia logic
        :param list_of_files: List of template files
        """
        print("ui.__init__")
        QtWidgets.QDialog.__init__(self)
        # load and show the user interface created with the designer.
        self.entrypoint = api
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__),'CassiopeiaUI.ui'))
        self.set_connections()

    def on_initialize(self):
        print("write to json")
        self.initialize_simulation()

    def on_start(self):
        print("connect button pressed")
        delta_t = self.ui.hsStep.value()
        print(delta_t)
        self.entrypoint.start_simulation(delta_t)

    def on_stop(self):
        print("disconnect button pressed")
        self.entrypoint.stop_simulation()

    def initialize_simulation(self):
        print("ui.initialize_simulation")
        params = self.get_parameters()
        self.entrypoint.initialize_simulation(params)

    def get_parameters(self):
        print("setparams")
        params = [self.ui.hsPlanetCount.value(), #planet_amount
                 self.ui.hsCentralMass.value(), #black_hole_mass
                 self.ui.hsPlanetMinRad.value(), #min_planet_radius
                 self.ui.hsPlanetMaxRad.value(), #max_planet_radius
                 self.ui.hsPlanetMinMass.value(), #min_planet_mass
                 self.ui.hsPlanetMaxMass.value(), #max_planet_mass
                 self.ui.sbSpaceX.value(), #space_
                 self.ui.sbSpaceY.value(), #space_y
                 self.ui.sbSpaceZ.value()] #space_z
        return params

    def set_connections(self):
        print("ui.set_connections")
        self.ui.btnStart.clicked.connect(self.on_start)
        self.ui.btnStop.clicked.connect(self.on_stop)
        self.ui.btnInitialize.clicked.connect(self.on_initialize)

        self.ui.hsStep.valueChanged.connect(self.on_hs_step_change)
        self.ui.leStep.textChanged.connect(self.on_le_step_change)
        self.ui.leCentralMass.textChanged.connect(self.on_le_cm_change)
        self.ui.hsCentralMass.valueChanged.connect(self.on_hs_cm_change)
        self.ui.lePlanetMinRad.textChanged.connect(self.on_le_pminr_change)
        self.ui.hsPlanetMinRad.valueChanged.connect(self.on_hs_pminr_change)
        self.ui.lePlanetMaxRad.textChanged.connect(self.on_le_pmaxr_change)
        self.ui.hsPlanetMaxRad.valueChanged.connect(self.on_hs_pmaxr_change)
        self.ui.lePlanetMaxMass.textChanged.connect(self.on_le_pmaxm_change)
        self.ui.hsPlanetMaxMass.valueChanged.connect(self.on_hs_pmaxm_change)
        self.ui.lePlanetMinMass.textChanged.connect(self.on_le_pminm_change)
        self.ui.hsPlanetMinMass.valueChanged.connect(self.on_hs_pminm_change)
        self.ui.lePlanetCount.textChanged.connect(self.on_le_pc_change)
        self.ui.hsPlanetCount.valueChanged.connect(self.on_hs_pc_change)

    #Setzen der Slider/List edit connection nicht schön aber selten, tbh idc
    def on_hs_step_change(self):
        self.ui.leStep.setText(str(self.ui.hsStep.value()))

    def on_le_step_change(self):
        self.ui.hsStep.setValue(int(self.ui.leStep.text()))

    def on_hs_cm_change(self):
        self.ui.leCentralMass.setText(str(self.ui.hsCentralMass.value()))

    def on_le_cm_change(self):
        self.ui.hsCentralMass.setValue(int(self.ui.leCentralMass.text()))

    def on_hs_pminr_change(self):
        self.ui.lePlanetMinRad.setText(str(self.ui.hsPlanetMinRad.value()))

    def on_le_pminr_change(self):
        self.ui.hsPlanetMinRad.setValue(int(self.ui.lePlanetMinRad.text()))

    def on_hs_pmaxr_change(self):
        self.ui.lePlanetMaxRad.setText(str(self.ui.hsPlanetMaxRad.value()))

    def on_le_pmaxr_change(self):
        self.ui.hsPlanetMaxRad.setValue(int(self.ui.lePlanetMaxRad.text()))

    def on_hs_pmaxm_change(self):
        self.ui.lePlanetMaxMass.setText(str(self.ui.hsPlanetMaxMass.value()))

    def on_le_pmaxm_change(self):
        self.ui.hsPlanetMaxMass.setValue(int(self.ui.lePlanetMaxMass.text()))

    def on_hs_pminm_change(self):
        self.ui.lePlanetMinMass.setText(str(self.ui.hsPlanetMinMass.value()))

    def on_le_pminm_change(self):
        self.ui.hsPlanetMinMass.setValue(int(self.ui.lePlanetMinMass.text()))

    def on_hs_pc_change(self):
        self.ui.lePlanetCount.setText(str(self.ui.hsPlanetCount.value()))

    def on_le_pc_change(self):
        self.ui.hsPlanetCount.setValue(int(self.ui.lePlanetCount.text()))

    def pause_simulation(self):
        print("ui.pause_simulation")
        self.ui.close()
