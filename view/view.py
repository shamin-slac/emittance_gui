from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QSpinBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout, QComboBox, QFileDialog, 
    QTableWidget, QTableWidgetItem, QAbstractScrollArea, 
    QHeaderView, QSizePolicy, QStackedWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from controller.controller import Controller

class View(QMainWindow):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle('Emittance Measurement')
        self.setGeometry(100, 100, 1800, 950)

        self.initUI()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.beamline_box = QComboBox()

        beamline_items = self.controller.load_beamlines()
        self.beamline_box.addItems(beamline_items)
        self.beamline_box.setCurrentIndex(-1)

        self.measurement_type_box = QComboBox()
        self.measurement_type_box.addItems(["Quad Scan", "Multi Device"])
        self.measurement_type_box.currentIndexChanged.connect(self.switch_measurement_type)

        self.stack = QStackedWidget()

        # options for quad scan
        page_quad = QWidget()
        quad_layout = QVBoxLayout(page_quad)
        form_layout_quad = QFormLayout()

        # options for multi device
        page_multi = QWidget()
        multi_layout = QVBoxLayout(page_multi)
        
        # Layout for form inputs
        
        self.profile_region_box = QComboBox()
        self.profile_devices_box = QComboBox()
        self.quad_region_box = QComboBox()
        self.quads_box = QComboBox()

        # Input fields
        self.energy_input = QLineEdit(self)
        self.scan_values_input = QLineEdit(self)
        self.n_shots_input = QSpinBox(self)
        
        self.energy_input.setPlaceholderText("Energy (GeV)")
        self.scan_values_input.setPlaceholderText("Scan Values (e.g., 1,2,3,4)")
        
        self.n_shots_input.setMinimum(1)
        self.n_shots_input.setMaximum(1000)

        # Adding to form layout
        form_layout_quad.addRow("Select beamline:", self.beamline_box)
        form_layout_quad.addRow("Select profile region:", self.profile_region_box)
        form_layout_quad.addRow("Select profile device:", self.profile_devices_box)
        form_layout_quad.addRow("Select quad region:", self.quad_region_box)
        form_layout_quad.addRow("Select quad:", self.quads_box)
        form_layout_quad.addRow("Energy (GeV):", self.energy_input)
        form_layout_quad.addRow("Scan Values (kG):", self.scan_values_input)
        form_layout_quad.addRow("Number of Shots:", self.n_shots_input)
        
        # Buttons
        self.run_button = QPushButton("Run Quadscan", self)
        self.abort_button = QPushButton("Abort", self)
        self.save_button = QPushButton("Save Data", self)
        self.load_button = QPushButton("Load Data", self)
        
        # Result table
        columns = ["x", "y"]
        rows = ["Emittance (mm-mrad)", "Beta (m)", "Alpha"]
        self.result_table = QTableWidget(len(rows), len(columns))
        self.result_table.setHorizontalHeaderLabels(columns)
        self.result_table.setVerticalHeaderLabels(rows)

        self.result_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Plot area
        self.matplotlib_widget = MatplotlibWidget(self)

        # Vertical layout with result table and plots
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_table)
        result_layout.addWidget(self.matplotlib_widget)
        result_layout.setStretch(0, 1)
        result_layout.setStretch(1, 4)

        # Connecting buttons to functions
        self.beamline_box.currentIndexChanged.connect(self.select_beamline)
        self.profile_region_box.currentIndexChanged.connect(self.select_profile_region)
        self.profile_devices_box.currentIndexChanged.connect(self.select_profile_device)
        self.quad_region_box.currentIndexChanged.connect(self.select_quad_region)
        self.quads_box.currentIndexChanged.connect(self.select_quad)
        self.run_button.clicked.connect(self.run_quadscan)
        self.abort_button.clicked.connect(self.abort_measurement)
        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data)
        
        # Add widgets to main layout
        # main_layout.addLayout(form_layout)
        quad_layout.addLayout(form_layout_quad)
        quad_layout.addWidget(self.run_button)
        quad_layout.addWidget(self.abort_button)
        main_layout.addLayout(result_layout)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.load_button)

        self.setCentralWidget(main_widget)

    def switch_measurement_type(self):
        
    
    def select_beamline(self):
        self.controller.select_beamline(self.beamline_box.currentText())
        region_items = self.controller.load_regions(self.beamline_box.currentText())
        self.profile_region_box.clear()
        self.profile_region_box.addItems(region_items)
        self.quad_region_box.clear()
        self.quad_region_box.addItems(region_items)

    def select_profile_region(self):
        if self.profile_region_box.currentIndex() != -1:
            self.controller.select_profile_region(self.profile_region_box.currentText())
            self.quad_region_box.setCurrentText(self.profile_region_box.currentText())
            profile_device_items = self.controller.load_profile_devices(self.profile_region_box.currentText())
            self.profile_devices_box.clear()
            self.profile_devices_box.addItems(profile_device_items)

    def select_profile_device(self):
        if self.profile_devices_box.currentIndex() != -1:    
            self.controller.select_profile_device(self.profile_devices_box.currentText())

    def select_quad_region(self):
        if self.quad_region_box.currentIndex() != -1:
            self.controller.select_quad_region(self.quad_region_box.currentText())
            quad_items = self.controller.load_quads(self.quad_region_box.currentText())
            self.quads_box.clear()
            self.quads_box.addItems(quad_items)

    def select_quad(self):
        if self.quads_box.currentIndex() != -1:    
            self.controller.select_quad(self.quads_box.currentText())
    
    def run_quadscan(self):
        # Gather input data
        emit_params = {
            "energy": float(self.energy_input.text()),
            "scan_values": list(map(float, self.scan_values_input.text().split(','))),
            "beamline": self.beamline_box.currentText(),
            "magnet_area": self.quad_region_box.currentText(),
            "magnet_name": self.quads_box.currentText(),
            "profile_device_area": self.profile_region_box.currentText(),
            "profile_device_name": self.profile_devices_box.currentText(),
            "n_shots": self.n_shots_input.value(),
        }

        # Use controller to process the quadscan
        data, figure, ax = self.controller.quadscan_process(emit_params)

        # Populate table with emittance, beta, and alpha
        self.populate_table(data)

        # Display the plot (for simplicity, assume plot is saved as an image file)
        self.matplotlib_widget.update_plot(figure, ax)

    def run_multi(self):
        # Gather input data
        emit_params = {
            "energy": float(self.energy_input.text()),
            "scan_values": list(map(float, self.scan_values_input.text().split(','))),
            "beamline": self.beamline_box.currentText(),
            "magnet_area": self.quad_region_box.currentText(),
            "magnet_name": self.quads_box.currentText(),
            "profile_device_area": self.profile_region_box.currentText(),
            "profile_device_name": self.profile_devices_box.currentText(),
            "n_shots": self.n_shots_input.value(),
        }

        # Use controller to process the quadscan
        data, figure, ax = self.controller.multi_process(emit_params)

        # Populate table with emittance, beta, and alpha
        self.populate_table(data)

        # Display the plot (for simplicity, assume plot is saved as an image file)
        self.matplotlib_widget.update_plot(figure, ax)
    
    def abort_measurement(self):
        # Placeholder to handle abort logic
        self.controller.abort()
        print("Measurement aborted.")

    def save_data(self):
        # Save Emittance Measurement to h5 file
        #TODO: Use save dialog once datetime is preserved in emittance measurement
        """
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "HDF5 Files (*.h5);;All Files (*)", options=options)
        """
        self.controller.save_data()
    
    def load_data(self):
        # Load Emittance Measurement from h5 file
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "HDF5 Files (*.h5);;All Files (*)", options=options)
        data, figure, ax  = self.controller.load_data(filepath)

        self.populate_table(data)
        self.matplotlib_widget.update_plot(figure, ax)

    def populate_table(self, data):
        # Populate emittance and beam params into table
        emittance = data.emittance
        beta = [data.beam_matrix[0][0], data.beam_matrix[1][0]]
        alpha = [data.beam_matrix[0][1], data.beam_matrix[1][1]]
        self.result_table.setItem(0, 0, QTableWidgetItem(str(emittance[0])))
        self.result_table.setItem(0, 1, QTableWidgetItem(str(emittance[1])))
        self.result_table.setItem(1, 0, QTableWidgetItem(str(beta[0])))
        self.result_table.setItem(1, 1, QTableWidgetItem(str(beta[1])))
        self.result_table.setItem(2, 0, QTableWidgetItem(str(alpha[0])))
        self.result_table.setItem(2, 1, QTableWidgetItem(str(alpha[1])))

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initially set figure and ax to None (empty)
        self.figure, self.ax = None, None
        self.canvas = None  # Initially no canvas since no figure

        # Create a layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    def update_plot(self, figure, ax):
        """Update the plot with the new scan results."""
        self.figure, self.ax = figure, ax
        self.figure.tight_layout()
        
        # Create the canvas with the new figure and add it to the layout
        self.canvas = FigureCanvas(self.figure)
        # self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        
        # Clear the existing layout and add the new canvas
        layout = self.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        layout.addWidget(self.canvas)
        self.canvas.draw()