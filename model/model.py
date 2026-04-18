from typing import Any, List, Optional, Union

import numpy as np
from slac_devices.magnet import Magnet
from slac_devices.screen import Screen
from slac_devices.wire import Wire
from slac_measurements.emittance import compute_emit_bmag, normalize_emittance
from slac_measurements.measurement import Measurement
from slac_measurements.emittance_measurement import QuadScanEmittance, MultiDeviceEmittance
from slac_measurements.model_general_calcs import bdes_to_kmod, build_quad_rmat, get_optics_after_magnet, multi_device_optics
from slac_tools.common.frontend.plotting.emittance import plot_quad_scan_result
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
        measurement = QuadScanEmittance(
            energy=emit_params["energy"], 
            scan_values=emit_params["scan_values"], 
            magnet=emit_params["magnet"], 
            beamsize_measurement=emit_params["beamsize_measurement"],
        )
        result = measurement.measure()
        self.emit_params = emit_params
        self.load_data(result)
    '''

    def quadscan(self, emit_params):
        class EmittanceMeasurementResult:
            # Mock the structure of the EmittanceMeasurementResult class for the example
            def __init__(self):
                import numpy as np
                self.quadrupole_pv_values = [np.array([-10., -7.77777778, -5.55555556, -3.33333333,
                                                       -1.11111111, 1.11111111, 5.55555556, 7.77777778, 10.]), 
                                             np.array([-10., -3.33333333, -1.11111111, 1.11111111,
                                                       3.33333333, 5.55555556, 7.77777778, 10.])]
                self.quadrupole_focusing_strengths = [np.array([1,2,3,4,5,6,7,8,9]), np.array([1,2,3,4,5,6,7,8,9])]
                self.twiss_at_screen = [np.array([[4.45227821, -0.08799274, 0.22634316],
                                                   [2.61720712, 0.62549609, 0.53157633],
                                                   [1.3118672, 0.84197498, 1.30266377],
                                                   [0.52491869, 0.57234878, 2.52912147],
                                                   [0.24515433, -0.17260647, 4.20059064],
                                                   [0.46149829, -1.38224251, 6.30683667],
                                                   [2.33885879, -5.15359673, 11.78333612],
                                                   [3.97837153, -7.69464818, 15.13373253],
                                                   [6.07098295, -10.65904497, 18.87918984]]),
                                        np.array([[3.87723245, -6.6080666, 11.52021312],
                                                  [0.94793842, -2.05478565, 5.50894868],
                                                  [0.53234745, -1.06149277, 3.99507294],
                                                  [0.40792976, -0.34076812, 2.73606637],
                                                  [0.58125328, 0.10107476, 1.73799641],
                                                  [1.05896415, 0.25764626, 1.00700443],
                                                  [1.84778742, 0.12248011, 0.54930636],
                                                  [2.95452759, -0.31096725, 0.37119323]])]
                self.rms_beamsizes = [np.array([2.11004182e-04, 1.61777833e-04, 1.14536742e-04,
                                                7.24512720e-05, 4.95130807e-05, 6.79336517e-05,
                                                1.52933266e-04, 1.99458518e-04, 2.46393640e-04]),
                                    np.array([0.00062267, 0.00030789, 0.00023073,
                                              0.00020197, 0.00024109, 0.00032542,
                                              0.00042986, 0.00054356])]
                self.beam_matrix = np.array([[1,2,3],[4,5,6]])
                self.emittance = np.array([0.01, 0.09999997])
                self.bmag = [np.array([9.36189932, 5.66900405, 3.05982085,
                                       1.51113423, 1.00000002, 1.5037432,
                                       5.46649484, 8.88148009, 13.22329213]),
                            np.array([3.79730158, 1.17877574, 1.00000001,
                                      1.18141181, 1.73104511, 2.65702909,
                                      3.96758895, 5.67104666])]
                self.metadata = []
            
            def __iter__(self):
                return iter(self.__dict__.items())
        
        self.load_data(EmittanceMeasurementResult())

    def multi(self, emit_params):
        measurement = MultiDeviceEmittance(
            energy=emit_params["energy"], 
            beamsize_measurements=emit_params["beamsize_measurements"],
        )
        result = measurement.measure()
        self.emit_params = emit_params
        self.load_data(result)
    
    def abort_measurement(self):
        pass

    def plot_data(self, emittance_result):
        return plot_quad_scan_result(emittance_result)
    
    def load_data(self, emittance_result):
        self.previous_data = self.current_data
        self.current_data = emittance_result
    

class AppConfig(BaseModel):
    """Holds application configuration

    Attributes:
    ------------------------
    
    """
    beamline: str = ""
    profile_region: str = ""
    quad_region: str = ""
    measurement_type: str = ""
    profile_device: List[str] = []
    quad: str = ""
    quad_values: List[float] = []
