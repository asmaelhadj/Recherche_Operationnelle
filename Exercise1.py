import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog, QDialog, QHeaderView
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PL1 import solve_blending_problem

class BlendingInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blending Problem Optimizer")
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Background Image
        self.background_label = QLabel(self.central_widget)
        pixmap = QPixmap("background_image.jpg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Main Layout with Transparent Background
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.variable_names = []
        self.variable_semantics = []
        self.constraints = []
        self.constraint_semantics = []
        self.variable_coefficients = []

        self.init_ui()

    def init_ui(self):
        title_label = QLabel("Blending Problem Optimizer")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #34495E;")
        self.main_layout.addWidget(title_label)

        self.main_layout.addWidget(QLabel("Objective Function (Minimize Cost)"))

        self.objective_table = QTableWidget(0, 3)
        self.objective_table.setHorizontalHeaderLabels(["Ingredient", "Cost Coefficient", "Description"])
        self.objective_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.objective_table)

        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        self.add_variable_btn = QPushButton("Add Ingredient")
        self.add_variable_btn.clicked.connect(self.add_variable)
        self.add_variable_btn.setStyleSheet(self.get_button_style("#1AA7EC"))
        button_layout.addWidget(self.add_variable_btn)

        self.delete_variable_btn = QPushButton("Delete Ingredient")
        self.delete_variable_btn.clicked.connect(self.delete_variable)
        self.delete_variable_btn.setStyleSheet(self.get_button_style("#C40C0C"))
        button_layout.addWidget(self.delete_variable_btn)

        self.main_layout.addWidget(QLabel("Constraints"))

        self.constraints_table = QTableWidget(0, 4)
        self.constraints_table.setHorizontalHeaderLabels(["Constraint Expression", "Relation", "Value", "Description"])
        self.constraints_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.constraints_table)

        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        self.add_constraint_btn = QPushButton("Add Constraint")
        self.add_constraint_btn.clicked.connect(self.add_constraint)
        self.add_constraint_btn.setStyleSheet(self.get_button_style("#1AA7EC"))
        button_layout.addWidget(self.add_constraint_btn)

        self.delete_constraint_btn = QPushButton("Delete Constraint")
        self.delete_constraint_btn.clicked.connect(self.delete_constraint)
        self.delete_constraint_btn.setStyleSheet(self.get_button_style("#C40C0C"))
        button_layout.addWidget(self.delete_constraint_btn)

        self.optimize_btn = QPushButton("Calculate Optimal Blend")
        self.optimize_btn.clicked.connect(self.optimize)
        self.optimize_btn.setStyleSheet(self.get_button_style("#1E0342"))
        self.main_layout.addWidget(self.optimize_btn)

    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12pt;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #2980B9;
            }}
        """

    def add_variable(self):
        var_name, ok = QInputDialog.getText(self, "Add Ingredient", "Enter the name of the ingredient:")
        if ok and var_name:
            coeff, ok = QInputDialog.getDouble(self, "Add Cost Coefficient", f"Enter the cost coefficient for {var_name}:")
            if ok:
                semantic_name, ok = QInputDialog.getText(self, "Add Description", f"Enter a description for {var_name}:")
                if ok:
                    self.variable_names.append(var_name)
                    self.variable_semantics.append(semantic_name)
                    self.variable_coefficients.append(coeff)
                    self.objective_table.insertRow(self.objective_table.rowCount())
                    self.objective_table.setItem(self.objective_table.rowCount() - 1, 0, QTableWidgetItem(var_name))
                    self.objective_table.setItem(self.objective_table.rowCount() - 1, 1, QTableWidgetItem(str(coeff)))
                    self.objective_table.setItem(self.objective_table.rowCount() - 1, 2, QTableWidgetItem(semantic_name))

    def delete_variable(self):
        row = self.objective_table.currentRow()
        if row != -1:
            self.variable_names.pop(row)
            self.variable_semantics.pop(row)
            self.variable_coefficients.pop(row)
            self.objective_table.removeRow(row)

    def add_constraint(self):
        expr, ok = QInputDialog.getText(self, "Add Constraint", "Enter the constraint expression (e.g., 3x + 2y):")
        if ok and expr:
            sense, ok = QInputDialog.getItem(self, "Add Relation", "Select the relation:", [">=", "<=", "="], 0, False)
            if ok:
                rhs, ok = QInputDialog.getDouble(self, "Add Value", "Enter the value for the constraint:")
                if ok:
                    semantic_name, ok = QInputDialog.getText(self, "Add Description", "Enter a description for the constraint:")
                    if ok:
                        self.constraints.append((expr, sense, rhs))
                        self.constraint_semantics.append(semantic_name)
                        self.constraints_table.insertRow(self.constraints_table.rowCount())
                        self.constraints_table.setItem(self.constraints_table.rowCount() - 1, 0, QTableWidgetItem(expr))
                        self.constraints_table.setItem(self.constraints_table.rowCount() - 1, 1, QTableWidgetItem(sense))
                        self.constraints_table.setItem(self.constraints_table.rowCount() - 1, 2, QTableWidgetItem(str(rhs)))
                        self.constraints_table.setItem(self.constraints_table.rowCount() - 1, 3, QTableWidgetItem(semantic_name))

    def delete_constraint(self):
        row = self.constraints_table.currentRow()
        if row != -1:
            self.constraints.pop(row)
            self.constraint_semantics.pop(row)
            self.constraints_table.removeRow(row)

    def optimize(self):
        results, objective_value = solve_blending_problem(self.variable_names, self.variable_coefficients, self.constraints)

        if results is not None:
            result_dialog = QDialog(self)
            result_layout = QVBoxLayout(result_dialog)
            result_table = QTableWidget(len(results), 2)
            result_table.setHorizontalHeaderLabels(["Ingredient", "Optimal Amount"])

            for i, (var, value) in enumerate(results.items()):
                result_table.setItem(i, 0, QTableWidgetItem(var))
                result_table.setItem(i, 1, QTableWidgetItem(str(value)))

            result_layout.addWidget(result_table)
            result_layout.addWidget(QLabel(f"Minimum Cost: {objective_value}"))
            result_dialog.setLayout(result_layout)
            result_dialog.setWindowTitle("Optimization Results")
            result_dialog.exec_()
        else:
            error_dialog = QDialog(self)
            error_layout = QVBoxLayout(error_dialog)
            error_layout.addWidget(QLabel("Optimization was not successful. Please check the inputs and try again."))
            error_dialog.setLayout(error_layout)
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlendingInterface()
    window.show()
    sys.exit(app.exec_())
