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
    QPushButton,
    QTextEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from ...Common import (
    KEY_BATTENEDCOL_SEC_PROFILE,
    KEY_BATTENEDCOL_SEC_PROFILE_OPTIONS_UI,
    KEY_BATTENEDCOL_SEC_SIZE,
    KEY_BATTENEDCOL_SEC_SIZE_OPTIONS_UI,
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
    KEY_BATTENEDCOL_BATTEN_PROFILE,
    KEY_BATTENEDCOL_BATTEN_PROFILE_OPTIONS_UI,
    KEY_BATTENEDCOL_BATTEN_PROFILE_OPTIONS,
    KEY_BATTENEDCOL_AXIAL_LOAD,
    KEY_BATTENEDCOL_CONN_TYPE,
    KEY_BATTENEDCOL_CONN_TYPE_OPTIONS,
    KEY_BATTENEDCOL_WELD_SIZE,
    KEY_BATTENEDCOL_WELD_SIZE_OPTIONS,
    KEY_BATTENEDCOL_BOLT_DIAMETER,
    KEY_BATTENEDCOL_BOLT_DIAMETER_OPTIONS,
    KEY_BATTENEDCOL_BOLT_TYPE,
    KEY_BATTENEDCOL_CUSTOM_SEC_SIZE,
    KEY_BATTENEDCOL_EFFECTIVE_AREA_OPTIONS,
    KEY_BATTENEDCOL_ALLOWABLE_UR_OPTIONS,
    KEY_BATTENEDCOL_WELD_SIZE_OPTIONS_UI,
    KEY_BATTENEDCOL_BOLT_DIAMETER_OPTIONS_UI,
    KEY_BATTENEDCOL_BOLT_TYPE_OPTIONS,
    KEY_DISP_BATTENEDCOL_BOLT_TYPE,
    KEY_BATTENEDCOL_EFFECTIVE_AREA,
    KEY_BATTENEDCOL_ALLOWABLE_UR,
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
    KEY_DISP_BATTENEDCOL_CONN_TYPE,
    KEY_DISP_BATTENEDCOL_EFFECTIVE_AREA,
    KEY_DISP_BATTENEDCOL_ALLOWABLE_UR,
    KEY_DISP_BATTENEDCOL_BOLT_DIAMETER,
    KEY_DISP_BATTENEDCOL_WELD_SIZE,
    KEY_DISP_BATTENEDCOL_BOLT_TYPE
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
        self.combo_batten_profile.addItems(KEY_BATTENEDCOL_BATTEN_PROFILE_OPTIONS_UI)
        self.combo_batten_section = QComboBox()
        self.combo_batten_section.addItems(KEY_BATTENEDCOL_BATTEN_PROFILE_OPTIONS)

        self.edit_axial_load = QLineEdit()
        self.combo_connection = QComboBox()
        self.combo_connection.addItems(KEY_BATTENEDCOL_CONN_TYPE_OPTIONS)

        # Preference controls
        self.combo_weld_size = QComboBox()
        self.combo_weld_size.addItems(KEY_BATTENEDCOL_WELD_SIZE_OPTIONS_UI)
        self.combo_bolt_dia = QComboBox()
        self.combo_bolt_dia.addItems(KEY_BATTENEDCOL_BOLT_DIAMETER_OPTIONS_UI)
        self.combo_bolt_type = QComboBox()
        self.combo_bolt_type.addItems(KEY_BATTENEDCOL_BOLT_TYPE_OPTIONS)
        self.combo_effective_area = QComboBox()
        self.combo_effective_area.addItems(KEY_BATTENEDCOL_EFFECTIVE_AREA_OPTIONS)
        self.combo_allowable_ur = QComboBox()
        self.combo_allowable_ur.addItems(KEY_BATTENEDCOL_ALLOWABLE_UR_OPTIONS)

        # Design action and summary
        self.btn_design = QPushButton("Design")
        self.btn_design.clicked.connect(self._on_design_clicked)
        self.summary_display = QTextEdit()
        self.summary_display.setReadOnly(True)
        
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
        form.addRow(KEY_DISP_BATTENEDCOL_SEC_PROFILE, self.combo_sec_profile)
        form.addRow(KEY_DISP_BATTENEDCOL_SEC_SIZE, self.combo_sec_size)
        form.addRow(self.lbl_custom_size, self.edit_custom_size)
        form.addRow(KEY_DISP_BATTENEDCOL_SPACING, self.edit_spacing)

        form.addRow(QLabel("<b>Material Properties</b>"))
        form.addRow(KEY_DISP_BATTENEDCOL_MATERIAL, self.combo_material)

        form.addRow(QLabel("<b>Geometry</b>"))
        form.addRow(KEY_DISP_BATTENEDCOL_UNSUPPORTED_LENGTH_YY, self.edit_lyy)
        form.addRow(KEY_DISP_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ, self.edit_lzz)

        form.addRow(QLabel("<b>End Conditions</b>"))
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_YY_1, self.combo_yy1)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_YY_2, self.combo_yy2)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_ZZ_1, self.combo_zz1)
        form.addRow(KEY_DISP_BATTENEDCOL_END_CONDITION_ZZ_2, self.combo_zz2)

        form.addRow(QLabel("<b>Battening</b>"))
        form.addRow(KEY_DISP_BATTENEDCOL_BATTEN_PROFILE, self.combo_batten_profile)

        form.addRow(QLabel("<b>Load and Connection</b>"))
        form.addRow(KEY_DISP_BATTENEDCOL_AXIAL_LOAD, self.edit_axial_load)
        form.addRow(KEY_DISP_BATTENEDCOL_CONN_TYPE, self.combo_connection)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_design)
        layout.addWidget(self.summary_display)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Inputs")

    def _create_pref_tab(self):
        tab = QWidget()
        prefs_tabs = QTabWidget()

        weld_tab = QWidget()
        weld_form = QFormLayout()
        weld_form.addRow(KEY_DISP_BATTENEDCOL_EFFECTIVE_AREA, self.combo_effective_area)
        weld_form.addRow(KEY_DISP_BATTENEDCOL_ALLOWABLE_UR, self.combo_allowable_ur)
        weld_form.addRow(KEY_DISP_BATTENEDCOL_BATTEN_PROFILE, self.combo_batten_section)
        weld_form.addRow(KEY_DISP_BATTENEDCOL_WELD_SIZE, self.combo_weld_size)
        weld_tab.setLayout(weld_form)

        bolt_tab = QWidget()
        bolt_form = QFormLayout()
        bolt_form.addRow(KEY_DISP_BATTENEDCOL_BOLT_DIAMETER, self.combo_bolt_dia)
        bolt_form.addRow(KEY_DISP_BATTENEDCOL_BOLT_TYPE, self.combo_bolt_type)
        bolt_tab.setLayout(bolt_form)

        prefs_tabs.addTab(weld_tab, "Weld Preferences")
        prefs_tabs.addTab(bolt_tab, "Bolt Preferences")

        layout = QVBoxLayout()
        layout.addWidget(prefs_tabs)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Design Preferences")

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

    def _collect_inputs(self):
        """Gather all input values into a dictionary."""
        data = {
            KEY_BATTENEDCOL_SEC_PROFILE: self.combo_sec_profile.currentText(),
            KEY_BATTENEDCOL_SEC_SIZE: self.combo_sec_size.currentText(),
            KEY_BATTENEDCOL_SPACING: self.edit_spacing.text(),
            KEY_BATTENEDCOL_MATERIAL: self.combo_material.currentText(),
            KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_YY: self.edit_lyy.text(),
            KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ: self.edit_lzz.text(),
            KEY_BATTENEDCOL_END_CONDITION_YY_1: self.combo_yy1.currentText(),
            KEY_BATTENEDCOL_END_CONDITION_YY_2: self.combo_yy2.currentText(),
            KEY_BATTENEDCOL_END_CONDITION_ZZ_1: self.combo_zz1.currentText(),
            KEY_BATTENEDCOL_END_CONDITION_ZZ_2: self.combo_zz2.currentText(),
            KEY_BATTENEDCOL_BATTEN_PROFILE: self.combo_batten_profile.currentText(),
            KEY_BATTENEDCOL_AXIAL_LOAD: self.edit_axial_load.text(),
            KEY_BATTENEDCOL_CONN_TYPE: self.combo_connection.currentText(),
            KEY_BATTENEDCOL_WELD_SIZE: self.combo_weld_size.currentText(),
            KEY_BATTENEDCOL_BOLT_DIAMETER: self.combo_bolt_dia.currentText(),
            KEY_BATTENEDCOL_BOLT_TYPE: self.combo_bolt_type.currentText(),
            KEY_BATTENEDCOL_EFFECTIVE_AREA: self.combo_effective_area.currentText(),
            KEY_BATTENEDCOL_ALLOWABLE_UR: self.combo_allowable_ur.currentText(),
        }
        if self.lbl_custom_size.isVisible():
            data[KEY_BATTENEDCOL_CUSTOM_SEC_SIZE] = self.edit_custom_size.text()
        if self.custom_material_data:
            data['custom_material'] = self.custom_material_data
        return data

    def _validate_inputs(self) -> bool:
        """Validate numeric inputs required for design."""
        errors = []
        try:
            axial = float(self.edit_axial_load.text())
            if axial <= 0:
                errors.append("Axial Load must be greater than 0.")
        except ValueError:
            errors.append("Axial Load must be a valid number greater than 0.")

        try:
            lyy = float(self.edit_lyy.text())
            if lyy <= 0:
                errors.append("Unsupported Length y-y must be greater than 0.")
        except ValueError:
            errors.append(
                "Unsupported Length y-y must be a valid number greater than 0."
            )

        try:
            lzz = float(self.edit_lzz.text())
            if lzz <= 0:
                errors.append("Unsupported Length z-z must be greater than 0.")
        except ValueError:
            errors.append(
                "Unsupported Length z-z must be a valid number greater than 0."
            )

        if errors:
            QMessageBox.warning(self, "Input Error", "\n".join(errors))
            return False
        return True

    def _on_design_clicked(self):
        """Show a dummy design summary using the collected inputs."""
        if not self._validate_inputs():
            return
        data = self._collect_inputs()
        summary = (
            f"Section: {data.get(KEY_BATTENEDCOL_SEC_PROFILE)}\n"
            f"Material: {data.get(KEY_BATTENEDCOL_MATERIAL)}\n"
            f"Load: {data.get(KEY_BATTENEDCOL_AXIAL_LOAD)} kN\n"
            f"Status: Safe"
        )
        self.summary_display.setPlainText(summary)

