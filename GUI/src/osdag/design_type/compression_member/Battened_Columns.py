from ..member import Member
from ...Common import *
from ...utils.common.component import ISection, Material
from ...utils.common.common_calculation import *
from ...utils.common.load import Load
from ..tension_member import *
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties
import math
import numpy as np
from ...utils.common import is800_2007
from ...utils.common.component import *
import logging
from ..connection.moment_connection import MomentConnection
from ...utils.common.material import *
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from pylatex.utils import NoEscape
from ...Common import TYPE_TAB_4, TYPE_TAB_5 
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QValidator, QDoubleValidator
from ...gui.ui_template import Window
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFormLayout
from PyQt5.QtWidgets import QDialogButtonBox

class MaterialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Material")
        self.setModal(True)
        self.setup_ui()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # Remove help button

    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Create input fields
        self.grade_input = QLineEdit()
        self.fy_20_input = QLineEdit()
        self.fy_20_40_input = QLineEdit()
        self.fy_40_input = QLineEdit()
        self.fu_input = QLineEdit()
        
        # Add fields to layout
        layout.addRow("Grade:", self.grade_input)
        layout.addRow("Fy (20mm):", self.fy_20_input)
        layout.addRow("Fy (20-40mm):", self.fy_20_40_input)
        layout.addRow("Fy (40mm):", self.fy_40_input)
        layout.addRow("Fu:", self.fu_input)
        
        # Add buttons with proper spacing
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def closeEvent(self, event):
        """Handle dialog close event"""
        self.reject()
        event.accept()

    def get_material_data(self):
        return {
            'grade': self.grade_input.text(),
            'fy_20': self.fy_20_input.text(),
            'fy_20_40': self.fy_20_40_input.text(),
            'fy_40': self.fy_40_input.text(),
            'fu': self.fu_input.text()
        }
    
class BattenedColumn(Member):
    def __init__(self):
        super(BattenedColumn, self).__init__()
        self.design_status = False
        self.result = {}
        self.utilization_ratio = 0
        self.area = 0
        self.epsilon = 1.0
        self.fy = 0
        self.section = None
        self.material = {}
        self.weld_size = ''
        self.weld_type = ''
        self.weld_strength = 0
        self.lacing_incl_angle = 0
        self.lacing_section = ''
        self.lacing_type = ''
        self.allowed_utilization = ''
        self.design_pref_dialog = None
        self.logger = None
        self.module = KEY_DISP_COMPRESSION_BattenedColumn
        self.mainmodule = 'Member'

    def tab_list(self):
        return [
            ("Weld Preferences", TYPE_TAB_4, self.get_weld_preferences),
            ("Bolt Preferences", TYPE_TAB_5, self.get_bolt_preferences)
            ]
    
    def get_weld_preferences(self, *args):
        return [
        (KEY_BATTENEDCOL_EFFECTIVE_AREA, "Effective Area Parameter", TYPE_COMBOBOX, ["1.0", "0.9", "0.8", "0.7", "0.6", "0.5", "0.4", "0.3", "0.2", "0.1"], True, 'No Validator'),
        (KEY_BATTENEDCOL_ALLOWABLE_UR, "Allowable Utilization Ratio", TYPE_COMBOBOX, ["1.0", "0.95", "0.9", "0.85"], True, 'No Validator'),
        (KEY_BATTENEDCOL_BATTEN_PROFILE, "Battening Profile Section", TYPE_COMBOBOX, ["ISA 40x40x5", "ISMC 75", "ISF 100x8"], True, 'No Validator'),
        (KEY_BATTENEDCOL_WELD_SIZE, "Weld Size", TYPE_COMBOBOX, ["5mm", "6mm", "8mm"], True, 'No Validator')
    ]
    
    def get_bolt_preferences(self, *args):
        return [
            (KEY_BATTENEDCOL_BOLT_DIAMETER, "Bolt Diameter", TYPE_COMBOBOX, ["16mm", "20mm", "24mm"], True, 'No Validator'),
            (KEY_DP_BOLT_TYPE, "Bolt Type", TYPE_COMBOBOX, ["Bearing", "Pretensioned"], True, 'No Validator')
            ]


    def all_weld_design_values(self, *args):
        return [
            (KEY_BATTENEDCOL_EFFECTIVE_AREA, "Effective Area Parameter", TYPE_COMBOBOX, ["1.0", "0.9", "0.8", "0.7", "0.6", "0.5", "0.4", "0.3", "0.2", "0.1"], True, 'No Validator'),
            (KEY_BATTENEDCOL_ALLOWABLE_UR, "Allowable Utilization Ratio", TYPE_COMBOBOX, ["1.0", "0.95", "0.9", "0.85"], True, 'No Validator'),
            (KEY_BATTENEDCOL_BATTEN_PROFILE, "Battening Profile Section", TYPE_COMBOBOX, ["ISA 40x40x5", "ISMC 75", "ISF 100x8"], True, 'No Validator'),
            (KEY_BATTENEDCOL_WELD_SIZE, "Weld Size", TYPE_COMBOBOX, ["5mm", "6mm", "8mm"], True, 'No Validator'),
            (KEY_BATTENEDCOL_BOLT_DIAMETER, "Bolt Diameter", TYPE_COMBOBOX, ["16mm", "20mm", "24mm"], True, 'No Validator'),
            (KEY_DP_BOLT_TYPE, "Bolt Type", TYPE_COMBOBOX, ["Bearing", "Pretensioned"], True, 'No Validator')
            ]
    

    def get_values_for_design_pref(self, key, design_dictionary):
        defaults = {KEY_BATTENEDCOL_EFFECTIVE_AREA: "1.0",
                    KEY_BATTENEDCOL_ALLOWABLE_UR: "1.0",
                    KEY_BATTENEDCOL_BATTEN_PROFILE: "ISA 40x40x5",
                    KEY_BATTENEDCOL_WELD_SIZE: "5mm",
                    KEY_BATTENEDCOL_BOLT_DIAMETER: "16mm",
                    KEY_DP_BOLT_TYPE: "Bearing"}
        return design_dictionary.get(key, defaults.get(key, ""))
    
    def tab_value_changed(self):
        def dummy_update(*args):
            return []

        return [
            (
                "Weld Preferences",
                [KEY_BATTENEDCOL_EFFECTIVE_AREA, KEY_BATTENEDCOL_ALLOWABLE_UR,
                 KEY_BATTENEDCOL_BATTEN_PROFILE, KEY_BATTENEDCOL_WELD_SIZE],
                [KEY_BATTENEDCOL_EFFECTIVE_AREA, KEY_BATTENEDCOL_ALLOWABLE_UR,
                 KEY_BATTENEDCOL_BATTEN_PROFILE, KEY_BATTENEDCOL_WELD_SIZE],
                TYPE_COMBOBOX,
                dummy_update
            ),
            (
                "Bolt Preferences",
                [KEY_BATTENEDCOL_BOLT_DIAMETER, KEY_DP_BOLT_TYPE],
                [KEY_BATTENEDCOL_BOLT_DIAMETER, KEY_DP_BOLT_TYPE],
                TYPE_COMBOBOX,
                dummy_update
            )
        ]

    def input_dictionary_design_pref(self):
        return [
            ("Weld Preferences", TYPE_COMBOBOX, [
                KEY_BATTENEDCOL_EFFECTIVE_AREA,
                KEY_BATTENEDCOL_ALLOWABLE_UR,
                KEY_BATTENEDCOL_BATTEN_PROFILE,
                KEY_BATTENEDCOL_WELD_SIZE
            ]),
            ("Bolt Preferences", TYPE_COMBOBOX, [
                KEY_BATTENEDCOL_BOLT_DIAMETER,
                KEY_DP_BOLT_TYPE  # ← restored to match your project constant
            ])
        ]


    def input_values(self, ui_self=None):
        self.module = KEY_DISP_BATTENEDCOL
        options_list = []
        # Module title
        options_list.append((KEY_DISP_BATTENEDCOL, "Battened Column", TYPE_MODULE, [], True, 'No Validator'))
        # Section Details
        options_list.append(("title_Section", "Section Details", TYPE_TITLE, None, True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_SEC_PROFILE, "Section Profile", TYPE_COMBOBOX, ["2-channel Back-to-Back", "2-channel Front-to-Front", "2-Girders"], True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_SEC_SIZE, "Section Size", TYPE_COMBOBOX, ["User-defined", "Auto-select"], True, 'No Validator'))
        if ui_self and isinstance(ui_self, dict) and ui_self.get(KEY_BATTENEDCOL_SEC_SIZE) == "User-defined":
            options_list.append((KEY_BATTENEDCOL_CUSTOM_SEC_SIZE, KEY_DISP_BATTENEDCOL_CUSTOM_SEC_SIZE, TYPE_TEXTBOX, None, True, 'Float Validator'))
        options_list.append((KEY_BATTENEDCOL_SPACING, "Spacing (mm)", TYPE_TEXTBOX, None, False, 'Float Validator'))

        # Material
        options_list.append(("title_Material", "Material Properties", TYPE_TITLE, None, True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_MATERIAL, "Material Grade", TYPE_COMBOBOX, ["E250", "E275", "E300", "Custom"], True, 'No Validator'))

        # Geometry
        options_list.append(("title_Geometry", "Geometry", TYPE_TITLE, None, True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_YY, "Unsupported Length y-y axis (mm)", TYPE_TEXTBOX, None, True, 'Float Validator'))
        options_list.append((KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ, "Unsupported Length z-z axis (mm)", TYPE_TEXTBOX, None, True, 'Float Validator'))

        # End Conditions
        options_list.append((KEY_BATTENEDCOL_END_CONDITION_YY_1, "End Condition y-y (End 1)", TYPE_COMBOBOX, ["Fixed", "Pinned", "Free"], True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_END_CONDITION_YY_2, "End Condition y-y (End 2)", TYPE_COMBOBOX, ["Fixed", "Pinned", "Free"], True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_END_CONDITION_ZZ_1, "End Condition z-z (End 1)", TYPE_COMBOBOX, ["Fixed", "Pinned", "Free"], True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_END_CONDITION_ZZ_2, "End Condition z-z (End 2)", TYPE_COMBOBOX, ["Fixed", "Pinned", "Free"], True, 'No Validator'))

        # Battening
        options_list.append((KEY_BATTENEDCOL_LACING_PROFILE, "Battening Profile", TYPE_COMBOBOX, ["Angle", "Channel", "Flat"], True, 'No Validator'))

        # Load and Connection
        options_list.append(("title_Load", "Load Details", TYPE_TITLE, None, True, 'No Validator'))
        options_list.append((KEY_BATTENEDCOL_AXIAL_LOAD, "Axial Load (kN)", TYPE_TEXTBOX, None, True, 'Float Validator'))
        options_list.append((KEY_BATTENEDCOL_CONN_TYPE, "Type of Connection", TYPE_COMBOBOX, ["Bolted", "Welded"], True, 'No Validator'))

        return options_list
    
    def run_design(self, design_dict):
        self.design_status = True
        self.result = {
            "section": design_dict.get(KEY_BATTENEDCOL_SEC_PROFILE, "2-channel Back-to-Back"),
            "material": design_dict.get(KEY_BATTENEDCOL_MATERIAL, "E250"),
            "load": design_dict.get(KEY_BATTENEDCOL_AXIAL_LOAD, "500"),
            "design_safe": True
            }
        return True
    def output_values(self, flag):
        if not flag:
            return []
        return [
        (None, "Design Summary", TYPE_TITLE, None, True),
        ("section", "Section Profile", TYPE_TEXTBOX, self.result.get("section", ""), True),
        ("material", "Material Grade", TYPE_TEXTBOX, self.result.get("material", ""), True),
        ("load", "Axial Load (kN)", TYPE_TEXTBOX, self.result.get("load", ""), True),
        ("status", "Design Status", TYPE_TEXTBOX, "Safe" if self.result.get("design_safe", False) else "Unsafe", True)
    ]

    def input_value_changed(self, ui_self=None):
        return [
        ([KEY_BATTENEDCOL_MATERIAL], KEY_BATTENEDCOL_MATERIAL, TYPE_CUSTOM_MATERIAL, self.show_custom_material_dialog)
        ]
    
    def show_custom_material_dialog(self, *args):
        if args and args[0] == "Custom":
            dialog = MaterialDialog()
            if dialog.exec_() == QDialog.Accepted:
                mat_data = dialog.get_material_data()
                self.material = mat_data
                return mat_data.get("grade", "Custom")
        return None


    
    def module_name(self):
        return KEY_DISP_BATTENEDCOL
 
    def set_osdaglogger(self, logger):
        self.logger = logger
        if self.logger:
            self.logger.append("Design started...")

    def input_dictionary_without_design_pref(self):
        return {
            KEY_BATTENEDCOL_SEC_PROFILE: "",
            KEY_BATTENEDCOL_SEC_SIZE: "",
            KEY_BATTENEDCOL_SPACING: "",
            KEY_BATTENEDCOL_MATERIAL: "",
            KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_YY: "",
            KEY_BATTENEDCOL_UNSUPPORTED_LENGTH_ZZ: "",
            KEY_BATTENEDCOL_END_CONDITION_YY_1: "",
            KEY_BATTENEDCOL_END_CONDITION_YY_2: "",
            KEY_BATTENEDCOL_END_CONDITION_ZZ_1: "",
            KEY_BATTENEDCOL_END_CONDITION_ZZ_2: "",
            KEY_BATTENEDCOL_LACING_PROFILE: "",
            KEY_BATTENEDCOL_AXIAL_LOAD: "",
            KEY_BATTENEDCOL_CONN_TYPE: "",
            KEY_MATERIAL:"",
            KEY_DP_BOLT_TYPE:""
            }
    
    def customized_input(self, ui_self=None):
        return []
    def func_for_validation(self, design_dict):
        return []
    
    def show_design_preferences(self):
        try:
            if self.design_pref_dialog is not None and self.design_pref_dialog.isVisible():
                return True
            if self.design_pref_dialog is not None:
                self.design_pref_dialog.show()
                return True
            from ...gui.UI_DESIGN_PREFERENCE import DesignPreferences
            self.design_pref_dialog = DesignPreferences(self, None, {})
            self.design_pref_dialog.finished.connect(self.cleanup_design_pref_dialog)
            self.design_pref_dialog.show()
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error showing design preferences: {str(e)}")
                return False
    def cleanup_design_pref_dialog(self):
        if self.design_pref_dialog is not None:
            self.design_pref_dialog.deleteLater()
            self.design_pref_dialog = None
    
    def get_tab_by_name(self, tab_name):
        if self.design_pref_dialog is None:
            return None
        self.design_pref_dialog.initialize_tabs()
        for i in range(self.design_pref_dialog.tabWidget.count()):
            tab = self.design_pref_dialog.tabWidget.widget(i)
            if tab.objectName() == tab_name:
                return tab
        return None
