import configparser
import os


class Config(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(path, 'game_config.ini')
        # print(config_path)
        self.path = config_path
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path)
    
    def get_PU(self, Pu_name, dd_name):
        # print(Pu_name, dd_name)
        # print(self.cf.sections())
        st = self.cf.get(Pu_name, dd_name)
        # print(self.cf.options('basics'))
        return st
    
    def get_sections(self):
        sections = self.cf.sections()
        return sections
    
    def get_options(self, PU):
        options = self.cf.options(PU)
        return options


if __name__ == '__main__':
    Config().get_PU('basics', 'welcome')
