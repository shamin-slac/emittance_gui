from datetime import datetime
from model.model import AppModel, AppConfig
from model.saving_loading import save_measurement_result, load_measurement_result

from lcls_tools.common.devices import yaml as lcls_yaml
from lcls_tools.common.devices.reader import create_magnet, create_screen, create_wire
from lcls_tools.common.measurements.screen_profile import ScreenBeamProfileMeasurement
# from lcls_tools.common.measurements.wire_scan import WireBeamProfileMeasurement
from lcls_tools.common.measurements.emittance_measurement import EmittanceMeasurementResult

import importlib.resources
import yaml

class Controller:
    def __init__(self, app_model: AppModel, app_config: AppConfig):
        self.app_model = app_model
        self.app_config = app_config

    def quadscan_process(self, emit_params):
        """
        Measure emittance using quad scan, plot beam sizes over scan
        
        Arguments
        ----------
        emit_params: Dictionary containing the following keys:
        `energy`, `scan_values`, `beamline`, `magnet_area`, `magnet_name`,
        `profile_device_area`, `profile_device_name`, `n_shots`
        """
        """
        quad = create_magnet(area=emit_params["magnet_area"], name=emit_params["magnet_name"])
        emit_params["magnet"] = quad
        if emit_params["profile_name"].startswith(("OTR", "YAG")):
            profile_device = create_screen(
                area=emit_params["profile_device_area"],
                name=emit_params["profile_device_name"],
            )
            emit_params["beamsize_measurement"] = ScreenBeamProfileMeasurement(
                beam_profile_device=profile_device,
                n_shots=emit_params["n_shots"],
            )
        elif emit_params["profile_name"].startswith("WS"):
            profile_device = create_wire(
                area=emit_params["profile_device_area"],
                name=emit_params["profile_device_name"],
            )
            emit_params["beamsize_measurement"] = WireBeamProfileMeasurement(
                beam_profile_device=profile_device,
                beampath=emit_params["beamline"],
            )
        else:
            raise ValueError("Profile device name prefix not recognized")
        """
        self.app_model.quadscan(emit_params)
        return self.app_model.current_data, *self.app_model.plot_data(self.app_model.current_data)
    
    def multi_process(self, emit_params):
        """
        Measure emittance using quad scan, plot beam sizes over scan
        
        Arguments
        ----------
        emit_params: Dictionary containing the following keys:
        `energy`, `beamline`, `profile_device_areas`, `profile_device_names`
        """
        self.app_model.multi(emit_params)
        return self.app_model.current_data, *self.app_model.plot_data(self.app_model.current_data)
    
    def abort(self):
        pass

    def save_data(self, filepath=None):
        if not filepath:
            current_datetime = datetime.now()
            filepath = "Emittance_measurement_" + current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + ".h5"
        save_measurement_result(self.app_model.current_data, filepath)

    def load_data(self, filepath):
        result = load_measurement_result(filepath, EmittanceMeasurementResult)
        self.app_model.load_data(result)
        return self.app_model.current_data, *self.app_model.plot_data(self.app_model.current_data)

    def analyze(self):
        pass

    def redo_point(self):
        # Get Data
        pass

    def save_config(self):
        pass

    def load_config(self):
        pass

    def logbook(self):
        pass

    def prof_to_log(self):
        pass

    def reset_quad(self):
        pass

    def set_quad(self):
        pass

    def upload_pvs(self):
        pass

    # Application configuration
    def load_beamlines(self):
        with importlib.resources.open_text(lcls_yaml, 'beampaths.yaml') as file:
            regions_by_beamline = yaml.load(file, Loader=yaml.FullLoader)
        
        return list(regions_by_beamline.keys())

    def select_beamline(self, beamline):
        self.app_config.beamline = beamline

    def load_regions(self, beamline):
        with importlib.resources.open_text(lcls_yaml, 'beampaths.yaml') as file:
            regions_by_beamline = yaml.load(file, Loader=yaml.FullLoader)
        nested_list = regions_by_beamline[beamline]

        regions_list = [item for sublist in nested_list for item in (sublist if isinstance(sublist, list) else [sublist])]

        return regions_list

    def select_profile_region(self, region):
        self.app_config.profile_region = region

    def select_measurement_type(self, measurement_type):
        pass

    def load_profile_devices(self, region):
        region_yaml = region + ".yaml"
        with importlib.resources.open_text(lcls_yaml, region_yaml) as file:
            devices = yaml.load(file, Loader=yaml.FullLoader)
        profile_devices = []
        if "screens" in devices.keys():
            profile_devices += list(devices["screens"].keys())
        if "wires" in devices.keys():
            profile_devices += list(devices["wires"].keys())

        return profile_devices
    
    def select_profile_device(self, profile_device):
        self.app_config.profile_device = profile_device

    def select_quad_region(self, region):
        self.app_config.quad_region = region
    
    def load_quads(self, region):
        region_yaml = region + ".yaml"
        with importlib.resources.open_text(lcls_yaml, region_yaml) as file:
            devices = yaml.load(file, Loader=yaml.FullLoader)
        quads = []
        if "magnets" in devices.keys():
            quads += list(devices["magnets"].keys())

        return quads

    def select_quad(self, quad):
        self.app_config.quad = quad

    def select_quad_values(self, quad_values):
        pass