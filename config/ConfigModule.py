import json
import shutil
from fileutils.FileUtilsModule import getAbsolutePath

CONFIG = 'config.json'
CONFIG_DEFAULT = 'config.json.default'


class Config(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            file = None
            try:
                file = open(getAbsolutePath(__file__, CONFIG), 'r')
            except:
                shutil.copy(getAbsolutePath(__file__, CONFIG_DEFAULT), getAbsolutePath(__file__, CONFIG))
                file = open(getAbsolutePath(__file__, CONFIG), 'r')

            cls.instance = super(Config, cls).__new__(cls)
            cls.instance.config = json.load(file)
            file.close

        return cls.instance

    def get(cls):
        return cls.instance.config

    def set(cls, config):
        cls.instance.config = config

        with open(getAbsolutePath(__file__, CONFIG), 'w') as outfile:
            json.dump(cls.instance.config, outfile)
