import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PLNE1 import solve_knapsack

class KnapsackApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("background_image.jpg").scaled(1024, 1000)))
        self.setPalette(palette)

        self.setWindowTitle("KnapSack Problem Solver")

    def initUI(self):
        self.setWindowTitle("KnapSack Problem Solver")

        window_width = 1000
        window_height = 600
        screen_geometry = app.primaryScreen().geometry()
        x_coordinate = int((screen_geometry.width() / 2) - (window_width / 2))
        y_coordinate = int((screen_geometry.height() / 2) - (window_height / 2))
        self.resize(window_width, window_height)
        self.move(x_coordinate, y_coordinate)


        self.project_name = QLabel("Knapsack Problem", self)
        self.project_name.setStyleSheet("color: #6AD4DD; font-family: Trebuchet MS; font-size: 24px;")  # Dark gray color, Arial font
        self.project_name.setAlignment(Qt.AlignCenter)

        self.project_description = QLabel("Enter Data:", self)
        self.project_description.setStyleSheet(
            "color: #FFFFFF; font-family: Trebuchet MS; font-size: 18px;")
        self.project_description.setAlignment(Qt.AlignCenter)

        self.valuesLabel = QLabel("Values (seperated by ','):", self)
        self.valuesEdit = QLineEdit(self)
        self.weightsLabel = QLabel("Weights (seperated by ','):", self)
        self.weightsEdit = QLineEdit(self)
        self.capacityLabel = QLabel("Capacity Of Sac:", self)
        self.capacityEdit = QLineEdit(self)

        self.solveButton = QPushButton("Optimize", self)

        self.resultTextEdit = QTextEdit(self)
        self.resultTextEdit.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.project_name)
        layout.addWidget(self.project_description)
        layout.addWidget(self.valuesLabel)
        layout.addWidget(self.valuesEdit)
        layout.addWidget(self.weightsLabel)
        layout.addWidget(self.weightsEdit)
        layout.addWidget(self.capacityLabel)
        layout.addWidget(self.capacityEdit)
        layout.addWidget(self.solveButton)
        layout.addWidget(self.resultTextEdit)

        self.solveButton.clicked.connect(self.solveKnapsack)

        self.applyStyles()

    def center(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = self.frameGeometry()
        x_coordinate = (screen_geometry.width() - window_geometry.width()) / 2
        y_coordinate = (screen_geometry.height() - window_geometry.height()) / 2
        self.move(x_coordinate, y_coordinate)

    def applyStyles(self):
        font = QFont("Trebuchet MS", 14, QFont.Bold)
        label_color = "#FFFFFF"  # White color
        label_style = f"color: {label_color};"
        label_font = font
        self.valuesLabel.setStyleSheet(label_style)
        self.valuesLabel.setFont(label_font)
        self.weightsLabel.setStyleSheet(label_style)
        self.weightsLabel.setFont(label_font)
        self.capacityLabel.setStyleSheet(label_style)
        self.capacityLabel.setFont(label_font)

        lineedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #FFFFFF; border-radius: 5px;"
        lineedit_font = font
        self.valuesEdit.setStyleSheet(lineedit_style)
        self.valuesEdit.setFont(lineedit_font)
        self.weightsEdit.setStyleSheet(lineedit_style)
        self.weightsEdit.setFont(lineedit_font)
        self.capacityEdit.setStyleSheet(lineedit_style)
        self.capacityEdit.setFont(lineedit_font)

        textedit_style = f"color: #FFFFFF; background-color: #2E2E2E; border: 2px solid #FFFFFF; border-radius: 5px;"
        textedit_font = font
        self.resultTextEdit.setStyleSheet(textedit_style)
        self.resultTextEdit.setFont(textedit_font)

        button_style = f"color: #FFFFFF; background-color: #6AD4DD; border: 2px solid #6AD4DD; border-radius: 5px;"
        button_font = font
        self.solveButton.setStyleSheet(button_style)
        self.solveButton.setFont(button_font)

    def solveKnapsack(self):
        values = [float(x) for x in self.valuesEdit.text().split(',')]
        weights = [float(x) for x in self.weightsEdit.text().split(',')]
        capacity = float(self.capacityEdit.text())

        total_value, selected_items = solve_knapsack(values, weights, capacity)

        result_str = f"Total Value: {int(total_value)}\n"
        result_str += "Chosen Products:\n"
        result_str += "\n".join(f"{value} of product {key + 1}" for key, value in selected_items.items())
        result_str += "\n"
        self.resultTextEdit.setPlainText(result_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex2_window = KnapsackApp()
    ex2_window.show()
    sys.exit(app.exec_())



    