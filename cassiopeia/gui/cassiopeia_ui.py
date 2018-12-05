import os

from PyQt5 import QtWidgets, uic


class CassiopeiaUi(QtWidgets.QMainWindow):

    def __init__(self, api, file_list):
        super(CassiopeiaUi, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "CassiopeiaUI.ui"), self)
        self.setWindowTitle("Cassiopeia setup")
        self.entry_point = api
        self.path_list = file_list
        self.set_list(file_list)
        self.set_connections()

    def set_list(self, list_of_files):
        """
        Extract the filename of the path to set into the ComboBox
        :param list_of_files: A list of json-file-paths from the Template folder
        """
        data_name = []
        for path in list_of_files:
            name_json = (str(path.split('\\')[-1]))
            name = (str(name_json.split(".")[0]))
            data_name.append(name)

        self.cmbTemplate.addItems(data_name)

    def set_connections(self):
        """
        Set all the Buttons,Labels,Sliders...
        """

        # Buttons

        self.btnStop.clicked.connect(self.on_stop)
        self.btnStart.clicked.connect(self.on_start)
        self.btnPause.clicked.connect(self.pause_simulation)
        self.btnInitialize.clicked.connect(self.on_initialize)

        # Textbox

        self.leStep.textChanged.connect(self.on_le_step_change)
        self.leCentralMass.textChanged.connect(self.on_le_cm_change)
        self.lePlanetCount.textChanged.connect(self.on_le_pc_change)
        self.lePlanetMinRad.textChanged.connect(self.on_le_pminr_change)
        self.lePlanetMaxRad.textChanged.connect(self.on_le_pmaxr_change)
        self.lePlanetMaxMass.textChanged.connect(self.on_le_pmaxm_change)
        self.lePlanetMinMass.textChanged.connect(self.on_le_pminm_change)

        # Slider

        self.hsStep.valueChanged.connect(self.on_hs_step_change)
        self.hsCentralMass.valueChanged.connect(self.on_hs_cm_change)
        self.hsPlanetCount.valueChanged.connect(self.on_hs_pc_change)
        self.hsPlanetMinRad.valueChanged.connect(self.on_hs_pminr_change)
        self.hsPlanetMaxRad.valueChanged.connect(self.on_hs_pmaxr_change)
        self.hsPlanetMaxMass.valueChanged.connect(self.on_hs_pmaxm_change)
        self.hsPlanetMinMass.valueChanged.connect(self.on_hs_pminm_change)

    def on_start(self):
        delta_t = self.hsStep.value()
        if self.cbTemplate.isChecked():
            index = self.cmbTemplate.currentIndex()
            self.entry_point.start_simulation(delta_t, self.path_list[index])
        else:
            self.entry_point.start_simulation(delta_t)

    def on_stop(self):
        self.entry_point.stop_simulation()

    def on_initialize(self):
        self.initialize_simulation()

    def on_hs_step_change(self):
        self.leStep.setText(str(self.hsStep.value()))

    def on_le_step_change(self):
        self.hsStep.setValue(int(self.leStep.text()))

    def on_hs_cm_change(self):
        self.leCentralMass.setText(str(self.hsCentralMass.value()))

    def on_le_cm_change(self):
        self.hsCentralMass.setValue(int(self.leCentralMass.text()))

    def on_hs_pminr_change(self):
        self.lePlanetMinRad.setText(str(self.hsPlanetMinRad.value()))

    def on_le_pminr_change(self):
        self.hsPlanetMinRad.setValue(int(self.lePlanetMinRad.text()))

    def on_hs_pmaxr_change(self):
        self.lePlanetMaxRad.setText(str(self.hsPlanetMaxRad.value()))

    def on_le_pmaxr_change(self):
        self.hsPlanetMaxRad.setValue(int(self.lePlanetMaxRad.text()))

    def on_hs_pmaxm_change(self):
        self.lePlanetMaxMass.setText(str(self.hsPlanetMaxMass.value()))

    def on_le_pmaxm_change(self):
        self.hsPlanetMaxMass.setValue(int(self.lePlanetMaxMass.text()))

    def on_hs_pminm_change(self):
        self.lePlanetMinMass.setText(str(self.hsPlanetMinMass.value()))

    def on_le_pminm_change(self):
        self.hsPlanetMinMass.setValue(int(self.lePlanetMinMass.text()))

    def on_hs_pc_change(self):
        self.lePlanetCount.setText(str(self.hsPlanetCount.value()))

    def on_le_pc_change(self):
        self.hsPlanetCount.setValue(int(self.lePlanetCount.text()))

    def pause_simulation(self):
        pass

    def initialize_simulation(self):
        print("Initialize simulation")
        params = self.get_parameters()
        self.entry_point.initialize_simulation(params)

    def get_parameters(self):
        """
        Collect all params form the cassiopeia setup
        :return: a list of params
        """
        print("Set chosen params")
        params = [self.hsPlanetCount.value(),  # planet_amount
                  self.hsCentralMass.value(),  # black_hole_mass
                  self.hsPlanetMinRad.value(),  # min_planet_radius
                  self.hsPlanetMaxRad.value(),  # max_planet_radius
                  self.hsPlanetMinMass.value(),  # min_planet_mass
                  self.hsPlanetMaxMass.value(),  # max_planet_mass
                  self.sbSpaceX.value(),  # space_
                  self.sbSpaceY.value(),  # space_y
                  self.sbSpaceZ.value()]  # space_z
        return params
