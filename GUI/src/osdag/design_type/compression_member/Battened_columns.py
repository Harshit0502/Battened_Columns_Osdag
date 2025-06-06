from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QFormLayout, QComboBox, QLineEdit,
    QLabel
)

from ...Common import (
    KEY_BATTENEDCOL_SEC_PROFILE,
    KEY_BATTENEDCOL_SEC_PROFILE_OPTIONS_UI,
    KEY_BATTENEDCOL_SEC_SIZE,
    KEY_BATTENEDCOL_SEC_SIZE_OPTIONS_UI,
    KEY_BATTENEDCOL_SEC_PROFILE_OPTIONS,
    KEY_BATTENEDCOL_SEC_SIZE,
    KEY_BATTENEDCOL_SEC_SIZE_OPTIONS
    KEY_BATTENEDCOL_SPACING,
    KEY_BATTENEDCOL_MATERIAL,
    KEY_BATTENEDCOL_MATERIAL_OPTIONS,
    KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_YY,
    KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ,
    KEY_BATTENEDCOL_END_CONDITION_OPTIONS,
    KEY_BATTENEDCOL_END_CONDITION_YY_1,
    KEY_BATTENEDCOL_END_CONDITION_YY_2,
    KEY_BATTENEDCOL_END_CONDITION_ZZ_1,
    KEY_BATTENEDCOL_END_CONDITION_ZZ_2,
    KEY_BATTENEDCOL_LACING_PROFILE,
    KEY_BATTENEDCOL_LACING_PROFILE_OPTIONS,
    KEY_BATTENEDCOL_AXIAL_LOAD,
    KEY_BATTENEDCOL_CONN_TYPE,
    KEY_BATTENEDCOL_CONN_TYPE_OPTIONS,
    KEY_BATTENEDCOL_WELD_SIZE,
    KEY_BATTENEDCOL_WELD_SIZE_OPTIONS,
    KEY_BATTENEDCOL_BOLT_DIAMETER,
    KEY_BATTENEDCOL_BOLT_DIAMETER_OPTIONS,
    KEY_BATTENEDCOL_EFFECTIVE_AREA,
    KEY_BATTENEDCOL_ALLOWABLE_UR,
    KEY_DISP_BATTENEDCOL_CUSTOM_SEC_SIZE
    KEY_BATTENEDCOL_ALLOWABLE_UR
)

class BattenedColumnInputWidget(QWidget):
    """UI widget for Battened Column input."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Battened Column")
        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        # Input controls
        self.combo_sec_profile = QComboBox()

        self.combo_sec_profile.addItems(KEY_BATTENEDCOL_SEC_PROFILE_OPTIONS_UI)

        self.combo_sec_size = QComboBox()
        self.combo_sec_size.addItems(KEY_BATTENEDCOL_SEC_SIZE_OPTIONS_UI)
        self.edit_custom_size = QLineEdit()
        self.lbl_custom_size = QLabel(KEY_DISP_BATTENEDCOL_CUSTOM_SEC_SIZE)
        self.lbl_custom_size.setVisible(False)
        self.edit_custom_size.setVisible(False)
        self.combo_sec_size.currentTextChanged.connect(self._toggle_custom_size)
        self.combo_sec_profile.addItems(KEY_BATTENEDCOL_SEC_PROFILE_OPTIONS)

        self.combo_sec_size = QComboBox()
        self.combo_sec_size.addItems(KEY_BATTENEDCOL_SEC_SIZE_OPTIONS)

        self.edit_spacing = QLineEdit()

        self.combo_material = QComboBox()
        self.combo_material.addItems(KEY_BATTENEDCOL_MATERIAL_OPTIONS)

        self.edit_lyy = QLineEdit()
        self.edit_lzz = QLineEdit()

        self.combo_yy1 = QComboBox()
        self.combo_yy1.addItems(KEY_BATTENEDCOL_END_CONDITION_OPTIONS)
        self.combo_yy2 = QComboBox()
        self.combo_yy2.addItems(KEY_BATTENEDCOL_END_CONDITION_OPTIONS)
        self.combo_zz1 = QComboBox()
        self.combo_zz1.addItems(KEY_BATTENEDCOL_END_CONDITION_OPTIONS)
        self.combo_zz2 = QComboBox()
        self.combo_zz2.addItems(KEY_BATTENEDCOL_END_CONDITION_OPTIONS)

        self.combo_batten_profile = QComboBox()
        self.combo_batten_profile.addItems(KEY_BATTENEDCOL_LACING_PROFILE_OPTIONS)

        self.edit_axial_load = QLineEdit()
        self.combo_connection = QComboBox()
        self.combo_connection.addItems(KEY_BATTENEDCOL_CONN_TYPE_OPTIONS)

        # Preference controls
        self.combo_weld_size = QComboBox()
        self.combo_weld_size.addItems(KEY_BATTENEDCOL_WELD_SIZE_OPTIONS)
        self.combo_bolt_dia = QComboBox()
        self.combo_bolt_dia.addItems(KEY_BATTENEDCOL_BOLT_DIAMETER_OPTIONS)
        self.combo_effective_area = QComboBox()
        self.combo_effective_area.addItems([
            "1.0", "0.9", "0.8", "0.7", "0.6", "0.5", "0.4", "0.3", "0.2", "0.1"
        ])
        self.combo_allowable_ur = QComboBox()
        self.combo_allowable_ur.addItems(["1.0", "0.95", "0.9", "0.85"])

    def _create_layout(self):
        self.tabs = QTabWidget()
        self._create_input_tab()
        self._create_pref_tab()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def _create_input_tab(self):
        tab = QWidget()
        form = QFormLayout()

        form.addRow(QLabel("<b>Section Details</b>"))
        form.addRow("Section Profile", self.combo_sec_profile)
        form.addRow("Section Size", self.combo_sec_size)
        form.addRow(self.lbl_custom_size, self.edit_custom_size)

        form.addRow("Spacing (mm)", self.edit_spacing)

        form.addRow(QLabel("<b>Material</b>"))
        form.addRow("Material Grade", self.combo_material)

        form.addRow(QLabel("<b>Geometry</b>"))
        form.addRow("Unsupported Length y-y (mm)", self.edit_lyy)
        form.addRow("Unsupported Length z-z (mm)", self.edit_lzz)

        form.addRow(QLabel("<b>End Conditions</b>"))
        form.addRow("y-y End 1", self.combo_yy1)
        form.addRow("y-y End 2", self.combo_yy2)
        form.addRow("z-z End 1", self.combo_zz1)
        form.addRow("z-z End 2", self.combo_zz2)

        form.addRow(QLabel("<b>Battening</b>"))
        form.addRow("Battening Profile", self.combo_batten_profile)

        form.addRow(QLabel("<b>Load and Connection</b>"))
        form.addRow("Axial Load (kN)", self.edit_axial_load)
        form.addRow("Type of Connection", self.combo_connection)

        tab.setLayout(form)
        self.tabs.addTab(tab, "Inputs")

    def _create_pref_tab(self):
        tab = QWidget()
        form = QFormLayout()
        form.addRow("Weld Size", self.combo_weld_size)
        form.addRow("Bolt Diameter", self.combo_bolt_dia)
        form.addRow("Effective Area Parameter", self.combo_effective_area)
        form.addRow("Allowable Utilization Ratio", self.combo_allowable_ur)
        tab.setLayout(form)
        self.tabs.addTab(tab, "Preferences")

    def _toggle_custom_size(self, text):
        show = text == 'User-defined'
        self.lbl_custom_size.setVisible(show)
        self.edit_custom_size.setVisible(show)

