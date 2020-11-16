
from configparser import ConfigParser
import os


class Config(object):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(path, 'game_config.ini')
        # print(config_path)
        self.path = config_path
        self.cf = ConfigParser()
        self.cf.read(self.path, encoding="utf-8-sig")
    
    def get_pu(self, pu_name, dd_name):
        # print(Pu_name, dd_name)
        # print(self.cf.sections())
        st = self.cf.get(pu_name, dd_name)
        # print(self.cf.options('basics'))
        return st
    
    def get_sections(self):
        sections = self.cf.sections()
        return sections
    
    def get_options(self, PU):
        options = self.cf.options(PU)
        return options


class Config_dict(ConfigParser):
    def __init__(self):
        self.conf_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base.ini')
        super().__init__()
        super().read(self.conf_name, encoding='utf-8')
    
    def save_data(self, section, option, value):
        super().set(section=section, option=option, value=value)
        super().write(fp=open(self.conf_name, 'w'))


if __name__ == '__main__':
    print(Config().get_pu('basics', 'welcome'))
    print(Config().get_pu('basics', 'goodbye'))
