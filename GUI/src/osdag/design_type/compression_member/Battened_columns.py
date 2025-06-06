from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QLabel,
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtCore import Qt
    KEY_BATTENEDCOL_BATTEN_PROFILE,
    KEY_BATTENEDCOL_BATTEN_PROFILE_OPTIONS,
    KEY_DISP_BATTENEDCOL_CUSTOM_SEC_SIZE,
    KEY_DISP_BATTENEDCOL_SEC_PROFILE,
    KEY_DISP_BATTENEDCOL_SEC_SIZE,
    KEY_DISP_BATTENEDCOL_SPACING,
    KEY_DISP_BATTENEDCOL_MATERIAL,
    KEY_DISP_BATTENEDCOL_UNSUPPORTED_LENGTH_YY,
    KEY_DISP_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ,
    KEY_DISP_BATTENEDCOL_END_CONDITION_YY_1,
    KEY_DISP_BATTENEDCOL_END_CONDITION_YY_2,
    KEY_DISP_BATTENEDCOL_END_CONDITION_ZZ_1,
    KEY_DISP_BATTENEDCOL_END_CONDITION_ZZ_2,
    KEY_DISP_BATTENEDCOL_BATTEN_PROFILE,
    KEY_DISP_BATTENEDCOL_AXIAL_LOAD,
    KEY_DISP_BATTENEDCOL_CONN_TYPE

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
)


class MaterialDialog(QDialog):
    """Dialog to capture custom material properties."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Material")
        self.setModal(True)
        self._setup_ui()
        # Remove the help button from the title bar
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def _setup_ui(self):
        layout = QFormLayout(self)

        self.grade_input = QLineEdit()
        self.fy20_input = QLineEdit()
        self.fy20_40_input = QLineEdit()
        self.fy40_input = QLineEdit()
        self.fu_input = QLineEdit()

        layout.addRow("Grade", self.grade_input)
        layout.addRow("Fy (20 mm)", self.fy20_input)
        layout.addRow("Fy (20–40 mm)", self.fy20_40_input)
        layout.addRow("Fy (40 mm)", self.fy40_input)
        layout.addRow("Fu", self.fu_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Return custom material data as a dictionary."""
        return {
            "grade": self.grade_input.text(),
            "fy_20": self.fy20_input.text(),
            "fy_20_40": self.fy20_40_input.text(),
            "fy_40": self.fy40_input.text(),
            "fu": self.fu_input.text(),
        }


class BattenedColumnInputWidget(QWidget):
    """UI widget for Battened Column input."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Battened Column")
        self._create_widgets()
        self._create_layout()
        self.custom_material_data = {}


        self.combo_batten_profile.addItems(KEY_BATTENEDCOL_BATTEN_PROFILE_OPTIONS)
        form.addRow(KEY_DISP_BATTENEDCOL_SEC_PROFILE, self.combo_sec_profile)
        form.addRow(KEY_DISP_BATTENEDCOL_SEC_SIZE, self.combo_sec_size)
        form.addRow(KEY_DISP_BATTENEDCOL_SPACING, self.edit_spacing)

        form.addRow(KEY_DISP_BATTENEDCOL_MATERIAL, self.combo_material)
        form.addRow(KEY_DISP_BATTENEDCOL_UNSUPPORTED_LENGTH_YY, self.edit_lyy)
        form.addRow(KEY_DISP_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ, self.edit_lzz)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_YY_1, self.combo_yy1)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_YY_2, self.combo_yy2)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_ZZ_1, self.combo_zz1)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_ZZ_2, self.combo_zz2)

        form.addRow(KEY_DISP_BATTENEDCOL_BATTEN_PROFILE, self.combo_batten_profile)

        form.addRow(KEY_DISP_BATTENEDCOL_AXIAL_LOAD, self.edit_axial_load)
        form.addRow(KEY_DISP_BATTENEDCOL_CONN_TYPE, self.combo_connection)

        self.edit_spacing = QLineEdit()

        self.combo_material = QComboBox()
        self.combo_material.addItems(KEY_BATTENEDCOL_MATERIAL_OPTIONS)
        self.combo_material.currentTextChanged.connect(self._handle_material_change)


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

        form.addRow(QLabel("<b>Material Properties</b>"))


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

    def _handle_material_change(self, text):
        """Open custom material dialog when required."""
        if text == 'Custom':
            dialog = MaterialDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                self.custom_material_data = dialog.get_data()
                grade = self.custom_material_data.get('grade') or 'Custom'
                self.combo_material.setCurrentText(grade)

