import yaml
import io

class Config:

    def __init__(self):  
        self.config_path = "config.yml"
        self.raw_config = self.parse_config()
        self.ignore_list = self.parse_ignore_list()
        self.test_pattern_list = self.parse_test_pattern_list()
        self.constants = self.parse_constants()

    def parse_config(self):
        with open(self.config_path, 'r') as stream:
            config = yaml.safe_load(stream)
        return config

    def parse_ignore_list(self):
        return self.raw_config.get("IGNORE_LIST")

    def parse_test_pattern_list(self):
        return self.raw_config.get("TEST_PATTERNS")

    def parse_constants(self):
        return self.raw_config["CONSTANTS"]
    