from configparser import ConfigParser

class Config:
    __conf = None

    def load_configuration():
        global __conf
        __conf = ConfigParser()
        __conf.read('properties.conf')

    def get(key: str):
        global __conf
        return __conf[key]