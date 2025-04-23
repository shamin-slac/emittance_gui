from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QSpinBox, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFormLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from controller.controller import Controller

class View(QMainWindow):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle('Emittance Measurement')
        self.setGeometry(100, 100, 900, 950)

        self.initUI()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.beamline_box = QComboBox()

        beamline_items = self.controller.load_beamlines()
        self.beamline_box.addItems(beamline_items)
        self.beamline_box.setCurrentIndex(-1)
        self.profile_region_box = QComboBox()
        self.profile_devices_box = QComboBox()
        self.quad_region_box = QComboBox()
        self.quads_box = QComboBox()
        
        # Layout for form inputs
        form_layout = QFormLayout()

        # Input fields
        self.energy_input = QLineEdit(self)
        self.scan_values_input = QLineEdit(self)
        self.n_shots_input = QSpinBox(self)
        self.magnet_input = QLineEdit(self)
        
        self.energy_input.setPlaceholderText("Energy (GeV)")
        self.scan_values_input.setPlaceholderText("Scan Values (e.g., 1,2,3,4)")
        self.magnet_input.setPlaceholderText("Magnet Parameters")
        
        self.n_shots_input.setMinimum(1)
        self.n_shots_input.setMaximum(1000)

        # Adding to form layout
        form_layout.addRow("Select beamline:", self.beamline_box)
        form_layout.addRow("Select profile region:", self.profile_region_box)
        form_layout.addRow("Select profile device:", self.profile_devices_box)
        form_layout.addRow("Select quad region:", self.quad_region_box)
        form_layout.addRow("Select quad:", self.quads_box)
        form_layout.addRow("Energy (GeV):", self.energy_input)
        form_layout.addRow("Scan Values:", self.scan_values_input)
        form_layout.addRow("Number of Shots:", self.n_shots_input)
        form_layout.addRow("Magnet:", self.magnet_input)
        
        # Buttons
        self.run_button = QPushButton("Run Quadscan", self)
        self.abort_button = QPushButton("Abort", self)

        # Plot area
        self.matplotlib_widget = MatplotlibWidget(self)

        # Connecting buttons to functions
        self.beamline_box.currentIndexChanged.connect(self.select_beamline)
        self.profile_region_box.currentIndexChanged.connect(self.select_profile_region)
        self.profile_devices_box.currentIndexChanged.connect(self.select_profile_device)
        self.quad_region_box.currentIndexChanged.connect(self.select_quad_region)
        self.quads_box.currentIndexChanged.connect(self.select_quad)
        self.run_button.clicked.connect(self.run_quadscan)
        self.abort_button.clicked.connect(self.abort_measurement)

        # Add widgets to main layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(self.abort_button)
        main_layout.addWidget(self.matplotlib_widget)

        self.setCentralWidget(main_widget)

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
            "magnet": self.magnet_input.text(),
            "n_measurement_shots": self.n_shots_input.value(),
            "beamsize_measurement": None,  # Example - you'd want to add actual measurement logic here
        }

        # Use controller to process the quadscan
        data, figure, ax = self.controller.quadscan_process(emit_params)

        # Display the plot (for simplicity, assume plot is saved as an image file)
        self.matplotlib_widget.update_plot(figure, ax)

    def abort_measurement(self):
        # Placeholder to handle abort logic
        self.controller.abort()
        print("Measurement aborted.")

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initially set figure and ax to None (empty)
        self.figure, self.ax = None, None
        self.canvas = None  # Initially no canvas since no figure

        # Create a layout
        layout = QVBoxLayout()
        self.setLayout(layout)

    def update_plot(self, figure, ax):
        """Update the plot with the new scan results."""
        self.figure, self.ax = figure, ax
        
        # Create the canvas with the new figure and add it to the layout
        self.canvas = FigureCanvas(self.figure)
        
        # Clear the existing layout and add the new canvas
        layout = self.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        layout.addWidget(self.canvas)
        self.canvas.draw()