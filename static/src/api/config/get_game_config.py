from configobj import ConfigObj
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
    
    def set_values(self, section, options, value):
        self.cf.set(section, options, value)
        self.cf.write(fp=open(self.path, 'w', encoding='utf-8'))
        return 'OK'


class Config_dict(ConfigParser):
    def __init__(self):
        self.conf_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game_config.ini')
        super().__init__()
        super().read(self.conf_name, encoding='utf-8')
    
    def save_data(self, section, option, value):
        super().set(section=section, option=option, value=value)
        super().write(fp=open(self.conf_name, 'w', encoding='utf-8'))
        

class Config_obj(object):  # Config_obj 方法读写配置文件
    def __init__(self):
        self.conf_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game_config.ini')
        self.config = ConfigObj(self.conf_name, encoding='utf-8')
    
    def update_option_or_values(self, section, option, values):
        self.config[section][option] = values
        self.config.write()
        
    def get_values(self, section, option):
        return self.config[section][option]


if __name__ == '__main__':
    # print(Config().get_pu('basics', 'welcome'))
    # print(Config().get_pu('basics', 'goodbye'))
    # cd = Config()
    # for r in cd.keys():
    #     print(r)
    #     if cd.items(r):
    #         for i in cd.items(r):
    #             print(i, type(i))
    # ass = cd.set_values('basics', 'an', '11')
    # print(ass)
    
    obj = Config_obj()
    print(obj.get_values('basics', 'luck_draw'))
    # obj.update_option_or_values('basics', 'an', '12')
    # obj = ConfigObj('./write_config.ini', encoding='utf-8')
    # obj.filename = './write_config.ini'
    # obj['basics'] = {}
    # obj['basics']['welcome'] = '欢迎1'
    # section2 = {'keyword5': 'value_5', 'keyword6': 'value_6', 'sub-section': {'keyword7': 'value_7'}}
    # obj['section2'] = section2
    # obj['section3'] = {}
    # obj['section3']['keyword 8'] = ['value_8', 'value_9', 'value_10']
    # obj['section3']['keyword 9'] = ['value_11', 'value_12', 'value_13']
    # obj.write()
    # print(ConfigObj('./write_config.ini'))
