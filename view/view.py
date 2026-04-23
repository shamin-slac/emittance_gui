from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QSpinBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QBuffer, Qt
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

        self.beamline_row = QHBoxLayout()
        self.beamline_label = QLabel("Select beamline:")
        self.beamline_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.beamline_label.setMinimumWidth(160)
        self.beamline_box = QComboBox()
        self.beamline_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.beamline_row.addWidget(self.beamline_label)
        self.beamline_row.addWidget(self.beamline_box)

        beamline_items = self.controller.load_beamlines()
        self.beamline_box.addItems(beamline_items)
        self.beamline_box.setCurrentIndex(-1)

        self.measurement_type_stack = QStackedWidget()

        self.measurement_type_row = QHBoxLayout()
        self.measurement_type_label = QLabel("Select measurement type:")
        self.measurement_type_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.measurement_type_label.setMinimumWidth(160)
        self.measurement_type_box = QComboBox()
        self.measurement_type_box.addItems(["Quad Scan", "Multi Device"])
        self.measurement_type_box.currentIndexChanged.connect(self.measurement_type_stack.setCurrentIndex)
        self.measurement_type_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.measurement_type_row.addWidget(self.measurement_type_label)
        self.measurement_type_row.addWidget(self.measurement_type_box)

        # options for quad scan
        page_quad = QWidget()
        quad_layout = QVBoxLayout(page_quad)
        form_layout_quad = QFormLayout()

        # options for multi device
        page_multi = QWidget()
        multi_layout = QVBoxLayout(page_multi)
        form_layout_multi = QFormLayout()
        
        # Layout for quad form inputs
        self.profile_region_box = QComboBox()
        self.profile_device_box = QComboBox()
        self.quad_region_box = QComboBox()
        self.quad_box = QComboBox()

        # Layout for multi form inputs
        self.multi_region_box = QComboBox()
        self.multi_list_box = QComboBox()

        # Quad Input fields
        self.quad_scan_energy_input = QLineEdit(self)
        self.scan_values_input = QLineEdit(self)
        self.n_shots_input = QSpinBox(self)
        
        self.quad_scan_energy_input.setPlaceholderText("Energy (GeV)")
        self.scan_values_input.setPlaceholderText("Scan Values (e.g., 1,2,3,4)")
        
        self.n_shots_input.setMinimum(1)
        self.n_shots_input.setMaximum(1000)

        self.multi_energy_input = QLineEdit(self)
        self.multi_energy_input.setPlaceholderText("Energy (GeV)")

        # Adding to quad form layout
        form_layout_quad.addRow("Select profile region:", self.profile_region_box)
        form_layout_quad.addRow("Select profile device:", self.profile_device_box)
        form_layout_quad.addRow("Select quad region:", self.quad_region_box)
        form_layout_quad.addRow("Select quad:", self.quad_box)
        form_layout_quad.addRow("Energy (GeV):", self.quad_scan_energy_input)
        form_layout_quad.addRow("Scan Values (kG):", self.scan_values_input)
        form_layout_quad.addRow("Number of Shots:", self.n_shots_input)

        # Adding to multi form layout
        form_layout_multi.addRow("Select multi device region:", self.multi_region_box)
        form_layout_multi.addRow("Select multi device list:", self.multi_list_box)
        form_layout_multi.addRow("Energy (GeV):", self.multi_energy_input)
        
        # Buttons
        self.run_quad_scan_button = QPushButton("Run Quadscan", self)
        self.run_multi_button = QPushButton("Run Multi Device Measurement", self)
        self.abort_quad_scan_button = QPushButton("Abort", self)
        self.abort_multi_button = QPushButton("Abort", self)
        self.log_button = QPushButton("Log Book GUI Screenshot", self)
        self.log_button.setStyleSheet("background-color: rgb(119, 241, 241);")
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
        self.profile_device_box.currentIndexChanged.connect(self.select_profile_device)
        self.quad_region_box.currentIndexChanged.connect(self.select_quad_region)
        self.quad_box.currentIndexChanged.connect(self.select_quad)
        self.multi_region_box.currentIndexChanged.connect(self.select_multi_device_region)
        self.multi_list_box.currentIndexChanged.connect(self.select_multi_device_list)
        self.run_quad_scan_button.clicked.connect(self.run_quadscan)
        self.run_multi_button.clicked.connect(self.run_multi)
        self.abort_quad_scan_button.clicked.connect(self.abort_measurement)
        self.abort_multi_button.clicked.connect(self.abort_measurement)
        self.log_button.clicked.connect(self.log_book)
        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data)
        
        # Add widgets to layouts
        # main_layout.addLayout(form_layout)
        quad_layout.addLayout(form_layout_quad)
        quad_layout.addWidget(self.run_quad_scan_button)
        quad_layout.addWidget(self.abort_quad_scan_button)

        multi_layout.addLayout(form_layout_multi)
        multi_layout.addWidget(self.run_multi_button)
        multi_layout.addWidget(self.abort_multi_button)

        self.measurement_type_stack.addWidget(page_quad)
        self.measurement_type_stack.addWidget(page_multi)

        main_layout.addLayout(self.beamline_row)
        main_layout.addLayout(self.measurement_type_row)
        main_layout.addWidget(self.measurement_type_stack)
        main_layout.addLayout(result_layout)
        main_layout.addWidget(self.log_button)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.load_button)

        self.setCentralWidget(main_widget)    
    
    def select_beamline(self):
        self.controller.select_beamline(self.beamline_box.currentText())
        region_items = self.controller.load_regions(self.beamline_box.currentText())
        multi_region_items = self.controller.load_multi_regions(self.beamline_box.currentText())
        self.profile_region_box.clear()
        self.profile_region_box.addItems(region_items)
        self.quad_region_box.clear()
        self.quad_region_box.addItems(region_items)
        self.multi_region_box.clear()
        self.multi_region_box.addItems(multi_region_items)

    def select_profile_region(self):
        if self.profile_region_box.currentIndex() != -1:
            self.controller.select_profile_region(self.profile_region_box.currentText())
            self.quad_region_box.setCurrentText(self.profile_region_box.currentText())
            profile_device_items = self.controller.load_profile_devices(self.profile_region_box.currentText())
            self.profile_device_box.clear()
            self.profile_device_box.addItems(profile_device_items)

    def select_profile_device(self):
        if self.profile_device_box.currentIndex() != -1:    
            self.controller.select_profile_device(self.profile_device_box.currentText())

    def select_quad_region(self):
        if self.quad_region_box.currentIndex() != -1:
            self.controller.select_quad_region(self.quad_region_box.currentText())
            quad_items = self.controller.load_quads(self.quad_region_box.currentText())
            self.quad_box.clear()
            self.quad_box.addItems(quad_items)

    def select_quad(self):
        if self.quad_box.currentIndex() != -1:    
            self.controller.select_quad(self.quad_box.currentText())

    def select_multi_device_region(self):
        if self.multi_region_box.currentIndex() != -1:
            self.controller.select_multi_device_region(self.multi_region_box.currentText())
            multi_device_list_items = self.controller.load_multi_device_lists(self.beamline_box.currentText(), self.multi_region_box.currentText())
            self.multi_list_box.clear()
            self.multi_list_box.addItems(multi_device_list_items)
    
    def select_multi_device_list(self):
        if self.multi_list_box.currentIndex() != -1:
            self.controller.select_multi_device_list(self.multi_list_box.currentText())
    
    def run_quadscan(self):
        # Gather input data
        emit_params = {
            "energy": float(self.quad_scan_energy_input.text()),
            "scan_values": list(map(float, self.scan_values_input.text().split(','))),
            "beamline": self.beamline_box.currentText(),
            "magnet_area": self.quad_region_box.currentText(),
            "magnet_name": self.quad_box.currentText(),
            "profile_device_area": self.profile_region_box.currentText(),
            "profile_device_name": self.profile_device_box.currentText(),
            "n_shots": self.n_shots_input.value(),
        }

        # Use controller to process the quadscan
        data, figure, ax = self.controller.quadscan_process(emit_params)

        # Populate table with emittance, beta, and alpha
        self.populate_table(data)

        # Display the plot (for simplicity, assume plot is saved as an image file)
        self.matplotlib_widget.update_plot(figure, ax)

    def run_multi(self):
        import json

        multi_device_dict = json.loads(self.multi_list_box.currentText())
        multi_device_names = list(multi_device_dict.keys())
        multi_device_areas = list(multi_device_dict.values())
        # Gather input data
        emit_params = {
            "energy": float(self.multi_energy_input.text()),
            "beamline": self.beamline_box.currentText(),
            "profile_device_areas": multi_device_areas,
            "profile_device_names": multi_device_names,
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

    def log_book(self):
        import physicselog as elog

        beampath = self.beamline_box.currentText()
        if beampath.startswith("SC"):
            logbook = "lcls2"
        elif beampath.startswith("CU"):
            logbook = "lcls"
        """
        else:
            self.logger.info(
                "Could not determine logbook for beampath %s",
                self.nav.beampath,
            )
            return
        """

        measurement_type = self.measurement_type_box.currentText()
        title = f"{measurement_type} Emittance"
        if measurement_type == "Multi Device":
            multi_device_list = self.multi_list_box.currentText()
            title += f" {multi_device_list}"
        elif measurement_type == "Quad Scan":
            quad = self.quad_box.currentText()
            beam_profile_device = self.profile_device_box.currentText()
            title += f" {quad} {beam_profile_device}"

        pixmap = self.grab()
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        pixmap.save(buffer, "PNG")

        """
        try:
            elog = importlib.import_module("physicselog")
        except Exception:
            self.logger.info("physicselog is unavailable in this environment")
            return
        """

        elog.submit_entry(
            logbook,
            "Wire Scan GUI",
            title,
            "",
            buffer.data(),
        )
        self.controller.save_data()
    
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