from model.model import AppModel, AppConfig

from lcls_tools.common.devices import yaml as lcls_yaml

import importlib.resources
import yaml

class Controller:
    def __init__(self, app_model: AppModel, app_config: AppConfig):
        self.app_model = app_model
        self.app_config = app_config

    def quadscan_process(self, emit_params):
        """Measure emittance using quad scan, plot beam sizes over scan
        """
        self.app_model.quadscan(emit_params)
        return self.app_model.current_data, *self.app_model.plot_data(self.app_model.current_data)
    
    def multidevice_process(self, emit_params):
        pass
    
    def abort(self):
        pass

    def save_data(self):
        pass

    def load_data(self):
        pass

    def analyze(self):
        pass

    # Get Data
    def redo_point(self):
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
            regions = yaml.load(file, Loader=yaml.FullLoader)
        nested_list = regions[beamline]

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