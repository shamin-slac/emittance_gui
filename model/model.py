from typing import Any, List, Optional
from lcls_tools.common.devices.magnet import Magnet
from lcls_tools.common.measurements.measurement import Measurement
from lcls_tools.common.measurements.emittance_measurement import QuadScanEmittance
from lcls_tools.common.frontend.plotting.emittance import plot_quad_scan_result
from meme.model import Model
from pydantic import BaseModel, PositiveInt

from model.plotting import plot_beam_size

class AppModel(BaseModel):
    """Holds attributes and data of emittance measurements

    Attributes:
    ------------------------
    emit_params: dict
        Dictionary containing emittance measurement parameters with the following keys: 
        `energy`, `scan_values`, `magnet`, `beamsize_measurement`, `n_measurement_shots`
    """
    emit_params: dict = {}
    lattice_model: object = None
    analysis_settings: dict = {}
    current_data: Any = {}
    previous_data: Any = {}
    status: str = None

    '''
    def quadscan(self, emit_params):
        measurement = QuadScanEmittance(emit_params["energy"], 
                                        emit_params["scan_values"], 
                                        emit_params["magnet"], 
                                        emit_params["beamsize_measurement"], 
                                        emit_params["n_measurement_shots"])
        results = measurement.measure()
        self.emit_params = emit_params
        self.previous_data = self.current_data
        self.current_data = results
    '''

    def quadscan(self, emit_params):
        class EmittanceMeasurementResult:
            # Mock the structure of the EmittanceMeasurementResult class for the example
            def __init__(self):
                import numpy as np
                self.quadrupole_pv_values = [np.array([0.1, 0.2, 0.3]), np.array([0.1, 0.2, 0.3])]
                self.twiss_at_screen = [np.array([[1.0], [2.0], [3.0]]), np.array([[1.0], [2.0], [3.0]])]
                self.rms_beamsizes = [np.array([0.5, 0.4, 0.3]), np.array([0.5, 0.4, 0.3])]
                self.emittance = [1e-6, 1e-6]
                self.bmag = [np.array([1.0, 1.2, 1.4]), np.array([1.0, 1.2, 1.4])]
        
        self.previous_data = self.current_data
        self.current_data = EmittanceMeasurementResult()

    def abort_measurement(self):
        pass

    def plot_data(self, emittance_result):
        return plot_quad_scan_result(emittance_result)
    
class AppConfig(BaseModel):
    """Holds application configuration

    Attributes:
    ------------------------
    
    """
    beamline: str = ""
    region: str = ""
    measurement_type: str = ""
    profile_devices: List[str] = []
    quad: str = ""
    quad_values: List[float] = []
