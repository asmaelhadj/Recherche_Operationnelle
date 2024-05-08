from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QComboBox, QSpinBox, QLabel)

from read_files import add_resource_to_product

REMOVE_BUTTON_COLOR = "#1AA7EC"
ADD_BUTTON_COLOR = "#1E2F97"
CALCULATE_BUTTON_COLOR = "#2980B9"
BUTTON_TEXT_COLOR = "white"
FONT_TYPE = "Roboto"
WINDOW_BACKGROUND_COLOR = "#ECF0F1"
NODE_PAIR_BACKGROUND_COLOR = "#D5DBDB"
INPUT_TEXT_COLOR = "#34495E"
LABEL_COLOR = "#34495E"
BIG_LABEL_COLOR = "#2C3E50"
LIGHT_BG_COLOR = "#FFFFFF"
TABLE_BACKGROUND_IMAGE = "background_image.jpg"  # Path to the background image


class ResourceManagementDialog(QDialog):
    def __init__(self, available_resources, current_product=None, parent=None):
        super().__init__(parent)
        self.current_product = current_product
        self.available_resources = available_resources
        self.setGeometry(100, 100, 1000, 600)

        self.setWindowTitle("Manage Product Resources")

        # Add background image
        background_label = QLabel(self)
        pixmap = QPixmap(TABLE_BACKGROUND_IMAGE)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, 1000, 600)

        layout = QVBoxLayout(self)

        # Table for adding/removing resources and specifying quantities
        self.resources_table = QTableWidget()
        self.resources_table.setColumnCount(3)
        self.resources_table.setHorizontalHeaderLabels(["Resource", "Quantity", "Remove"])
        layout.addWidget(self.resources_table)

        # Button to add a new row to specify a resource
        add_resource_btn = QPushButton("Add Resource")
        add_resource_btn.clicked.connect(self.add_resource_row)
        add_resource_btn.setStyleSheet(f"background-color: {ADD_BUTTON_COLOR}; color: {BUTTON_TEXT_COLOR};")
        layout.addWidget(add_resource_btn)

        # OK and Cancel buttons
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.apply_changes)
        ok_btn.setStyleSheet(f"background-color: {CALCULATE_BUTTON_COLOR}; color: {BUTTON_TEXT_COLOR};")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"background-color: {REMOVE_BUTTON_COLOR}; color: {BUTTON_TEXT_COLOR};")

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def apply_changes(self):
        print("clicked")
        if self.current_product is not None:
            # Clear existing resources needed for fresh input
            self.current_product["resources_needed"] = []
            for row in range(self.resources_table.rowCount()):
                resource_combo = self.resources_table.cellWidget(row, 0)
                qty_input = self.resources_table.cellWidget(row, 1)

                resource_name = resource_combo.currentText()
                quantity = qty_input.value()

                # Append new resource data to the product's resources_needed
                add_resource_to_product(self.current_product["name"], resource_name, quantity)

        self.accept()  # Close the dialog

    def add_resource_row(self):
        row_pos = self.resources_table.rowCount()
        self.resources_table.insertRow(row_pos)

        combo_box = QComboBox()
        for resource in self.available_resources:
            combo_box.addItem(resource["name"], resource)

        qty_input = QSpinBox()
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_resource_row(row_pos))

        self.resources_table.setCellWidget(row_pos, 0, combo_box)
        self.resources_table.setCellWidget(row_pos, 1, qty_input)
        self.resources_table.setCellWidget(row_pos, 2, remove_btn)

    def remove_resource_row(self, row_pos):
        self.resources_table.removeRow(row_pos)