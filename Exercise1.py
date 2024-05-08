import sys

from PyQt5 import QtGui

from PL1 import solve_optimization
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QSpinBox, QPushButton, \
    QVBoxLayout, QHBoxLayout, QMainWindow, QTabWidget, QLineEdit, QTableWidgetItem, \
    QDialog, QHeaderView, QDoubleSpinBox
from read_files import load_products, load_resources, add_product, add_resource, delete_product_from_json, \
    delete_resource_from_json

from ResourceManagementDialog import ResourceManagementDialog
def exit_program():
    app.quit()

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

class Exercise1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.font = QFont(FONT_TYPE)
        self.setFont(self.font)

        self.product_columns = ["Name", "Price", "Worker Time", "Machine Time"]
        self.products = load_products()
        self.resources = load_resources()
        self.current_product = None
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("Dynamic Production Planner")
        self.setGeometry(100, 100, 1000, 600)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create tabs
        self.product_management_tab = QWidget()
        self.resource_management_tab = QWidget()
        self.tab_widget.addTab(self.product_management_tab, "Product Management")
        self.tab_widget.addTab(self.resource_management_tab, "Resource Management")

        # Initialize UI Components for Each Tab
        self.setup_product_management_tab()
        self.setup_resource_management_tab()
        self.load_data_into_ui()

    def add_product_to_table(self, product):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)
        self.product_table.setItem(row_position, 0, QTableWidgetItem(product["name"]))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(str(product["Price"])))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(str(product["Worker_time"])))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(str(product["Machine_time"])))

    def add_resource_to_table(self, resource):
        row_position = self.resource_table.rowCount()
        self.resource_table.insertRow(row_position)
        # Convert numerical values to strings before setting them as table items
        self.resource_table.setItem(row_position, 0, QTableWidgetItem(resource["name"]))
        self.resource_table.setItem(row_position, 1, QTableWidgetItem(str(resource["quantity_available"])))

    def setup_product_management_tab(self):
        self.product_management_layout = QVBoxLayout(self.product_management_tab)
        self.setup_product_table()
        self.setup_product_form()
        self.update_button_state(self.product_fields, self.add_button, "Please fill in all fields to add a product.")

    def setup_product_table(self):
        self.product_table_widget = QLabel(self.product_management_tab)  # Use QLabel as the container
        self.product_table_widget.setGeometry(10, 10, 500, 200)  # Adjust the geometry as needed

        self.product_table = QTableWidget(self.product_table_widget)
        self.product_table.setGeometry(250, 0, 500, 300)  # Match geometry with the parent
        self.product_table.setColumnCount(len(self.product_columns))
        self.product_table.setHorizontalHeaderLabels(self.product_columns)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        pixmap = QPixmap(TABLE_BACKGROUND_IMAGE)
        self.product_table_widget.setPixmap(pixmap.scaled(self.product_table.size()))  # Set background image
        self.product_table_widget.setScaledContents(True)
        self.product_management_layout.addWidget(self.product_table_widget)

    def setup_resource_management_tab(self):
        self.resource_management_layout = QVBoxLayout(self.resource_management_tab)
        self.setup_resource_table()
        self.setup_resource_form()

    def setup_product_form(self):
        # Form layout
        self.product_form_layout = QHBoxLayout()
        self.product_management_layout.addLayout(self.product_form_layout)

        # Form fields
        self.name_input = QLineEdit()
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setMaximum(999999.99)
        self.human_work_time_input = QSpinBox()
        self.human_work_time_input.setMaximum(999999)
        self.machine_time_input = QSpinBox()
        self.machine_time_input.setMaximum(999999)

        self.product_fields = [self.name_input, self.selling_price_input, self.human_work_time_input,
                               self.machine_time_input]

        # Connect each field's textChanged signal
        for field in self.product_fields:
            field.textChanged.connect(lambda: self.update_button_state(self.product_fields, self.add_button,
                                                                       "Please fill in all fields to add a product."))

        self.product_form_layout.addWidget(QLabel("Name:"))
        self.product_form_layout.addWidget(self.name_input)

        self.product_form_layout.addWidget(QLabel("Selling Price:"))
        self.product_form_layout.addWidget(self.selling_price_input)

        self.product_form_layout.addWidget(QLabel("Human Work Time:"))
        self.product_form_layout.addWidget(self.human_work_time_input)

        self.product_form_layout.addWidget(QLabel("Machine Time:"))
        self.product_form_layout.addWidget(self.machine_time_input)

        self.manage_resources_btn = QPushButton("Manage Resources")
        self.manage_resources_btn.setFont(QFont("Montserrat", 7))
        self.manage_resources_btn.setFixedSize(100, 40)
        self.manage_resources_btn.setStyleSheet(
            f"background-color: {CALCULATE_BUTTON_COLOR}; color: {BUTTON_TEXT_COLOR};")
        self.manage_resources_btn.clicked.connect(self.manage_product_resources)
        self.product_form_layout.addWidget(self.manage_resources_btn)

        # Add and Delete buttons
        self.add_button = QPushButton("Add Product")
        self.add_button.setStyleSheet(f"background-color: {ADD_BUTTON_COLOR}; color: {BUTTON_TEXT_COLOR};")
        self.add_button.clicked.connect(self.add_product)
        self.product_management_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Selected Product")
        self.delete_button.setStyleSheet(f"background-color: {REMOVE_BUTTON_COLOR}; color: {BUTTON_TEXT_COLOR};")
        self.delete_button.clicked.connect(self.delete_product)
        self.product_management_layout.addWidget(self.delete_button)

        # Placeholder for Optimization button (Gurobi integration)
        self.optimize_button = QPushButton("Optimize Production Plan")
        self.optimize_button.clicked.connect(self.optimize_production_plan)
        self.product_management_layout.addWidget(self.optimize_button)

    def setup_resource_table(self):
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(2)
        self.resource_table.setHorizontalHeaderLabels(["Resource Name", "Quantity Available"])
        self.resource_management_layout.addWidget(self.resource_table)

    def manage_product_resources(self):
        self.current_product = {"name": self.name_input.text(), "Price": self.selling_price_input.value(),
                                "Worker_time": self.human_work_time_input.value(),
                                "Machine_time": self.machine_time_input.value(), "resources_needed": [], }
        add_product(self.current_product)
        self.resources = load_resources()
        dialog = ResourceManagementDialog(self.resources, self.current_product)
        if dialog.exec_() == QDialog.Accepted:
            # Gather data from dialog and update the product being added/edited
            pass

    def setup_resource_form(self):
        self.resource_form_layout = QHBoxLayout()
        self.resource_management_layout.addLayout(self.resource_form_layout)

        self.resource_name_input = QLineEdit()
        self.quantity_available_input = QSpinBox()
        self.quantity_available_input.setMaximum(99999999)
        self.resource_fields = [self.resource_name_input, self.quantity_available_input]

        for field in self.resource_fields:
            field.textChanged.connect(
                lambda: self.update_button_state(self.resource_fields, self.add_resource_button,
                                                 "Please enter a valid name and quantity to add a resource."))

        self.resource_form_layout.addWidget(QLabel("Resource Name:"))
        self.resource_form_layout.addWidget(self.resource_name_input)

        self.resource_form_layout.addWidget(QLabel("Quantity Available:"))
        self.resource_form_layout.addWidget(self.quantity_available_input)

        self.add_resource_button = QPushButton("Add Resource")
        self.add_resource_button.clicked.connect(self.add_resource)
        self.resource_management_layout.addWidget(self.add_resource_button)
        self.update_button_state(self.resource_fields, self.add_resource_button,
                                 "Please enter a valid name and quantity to add a resource.")

        self.delete_resource_button = QPushButton("Delete Selected Resource")
        self.delete_resource_button.clicked.connect(self.delete_resource)
        self.resource_management_layout.addWidget(self.delete_resource_button)

    def load_data_into_ui(self):
        self.products = load_products()
        self.resources = load_resources()
        print(self.products)

        # Clear existing rows in the tables
        self.product_table.setRowCount(0)
        self.resource_table.setRowCount(0)
        # Populate product table
        for product in self.products:
            self.add_product_to_table(product)

        # Populate resource table
        for resource in self.resources:
            self.add_resource_to_table(resource)

    def add_product(self):
        row_position = self.product_table.rowCount()
        self.product_table.insertRow(row_position)

        self.product_table.setItem(row_position, 0, QTableWidgetItem(self.name_input.text()))
        self.product_table.setItem(row_position, 1, QTableWidgetItem(str(self.selling_price_input.value())))
        self.product_table.setItem(row_position, 2, QTableWidgetItem(str(self.human_work_time_input.value())))
        self.product_table.setItem(row_position, 3, QTableWidgetItem(str(self.machine_time_input.value())))

        # FIXME: We removed this to prevent the product being saved twice (here and when adding ressources). See if there's a better way
        # new_product = {"name": self.name_input.text(), "selling_price": self.selling_price_input.text(),
        #                "human_work_time": self.human_work_time_input.text(),
        #                "machine_time": self.machine_time_input.text(), }
        # add_product(new_product)

        # Clear input fields after adding
        self.name_input.clear()
        self.selling_price_input.setValue(0)
        self.human_work_time_input.setValue(0)
        self.machine_time_input.setValue(0)

    def add_resource(self):
        row_position = self.resource_table.rowCount()
        self.resource_table.insertRow(row_position)
        self.resource_table.setItem(row_position, 0, QTableWidgetItem(self.resource_name_input.text()))
        self.resource_table.setItem(row_position, 1,
                                    QTableWidgetItem(str(self.quantity_available_input.value())))

        new_resource = {"name": self.resource_name_input.text(),
                        "quantity_available": self.quantity_available_input.value(), }
        add_resource(new_resource)
        self.resource_name_input.clear()
        self.quantity_available_input.setValue(0)

    def delete_resource(self):
        indices = self.resource_table.selectionModel().selectedRows()
        for index in sorted(indices, reverse=True):
            resource_name = self.product_table.item(index.row(), 0).text()
            delete_resource_from_json(resource_name)
            self.resource_table.removeRow(index.row())

    def delete_product(self):
        indices = self.product_table.selectionModel().selectedRows()
        for index in sorted(indices, reverse=True):
            product_name = self.product_table.item(index.row(), 0).text()
            delete_product_from_json(product_name)
            self.product_table.removeRow(index.row())

    @staticmethod
    def update_button_state(fields, button, tooltip_message):
        # Check if all the fields are non-empty
        is_all_fields_non_empty = all(field.text().strip() for field in fields)

        # Enable the button if all fields are non-empty, else disable it
        button.setEnabled(is_all_fields_non_empty)

        # Update tooltip based on the button's enabled state
        if not button.isEnabled():
            button.setToolTip(tooltip_message)
        else:
            button.setToolTip("")  # Clear tooltip when the button is enabled

    def optimize_production_plan(self):
        pl_optimizer = solve_optimization()
        optimized_plan, total_sales = pl_optimizer.optimize()

        result_dialog = QDialog(self)
        result_layout = QVBoxLayout(result_dialog)

        result_table = QTableWidget()
        result_table.setColumnCount(2)
        result_table.setHorizontalHeaderLabels(["Product", "Optimized Quantity"])
        for product, quantity in optimized_plan.items():
            row_position = result_table.rowCount()
            result_table.insertRow(row_position)
            result_table.setItem(row_position, 0, QTableWidgetItem(product))
            result_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))

        result_layout.addWidget(result_table)
        result_layout.addWidget(QLabel(f"Total Projected Sales: ${total_sales:,.2f}"))
        result_dialog.setLayout(result_layout)
        result_dialog.setWindowTitle("Optimization Results")
        result_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex1_window = Exercise1()
    ex1_window.show()
    sys.exit(app.exec_())
