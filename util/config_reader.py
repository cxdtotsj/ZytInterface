
import configparser


class ConfigReader:

    def __init__(self, config_path=None):
        self.rConfig = configparser.ConfigParser()
        if config_path is None:
            self.path = "../base/config.ini"
        else:
            self.path = config_path
        self.rConfig.read(self.path, encoding='utf-8')

    def get_section(self):
        return self.rConfig.sections()

    def get_value(self, section, option):
        return self.rConfig.get(section, option)

    def get_option(self, section):
        return self.rConfig.options(section)

    # 存在%号时，读取报错
    def get_items(self,section):
        return self.rConfig.items(section)


if __name__ == '__main__':
    rconfig = ConfigReader()
    a = rconfig.get_value("db_dev","db_username")
    print(a)