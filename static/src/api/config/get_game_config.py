import configparser
import os


class Config(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(path, 'game_config.ini')
        print(config_path)
        self.path = config_path
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path)
    
    def get_PU(self, Pu_name, dd_name):
        print(Pu_name, dd_name)
        print(self.cf.sections())
        st = self.cf.get(Pu_name, dd_name)
        return st


if __name__ == '__main__':
    Config().get_PU('basics', 'welcome')
