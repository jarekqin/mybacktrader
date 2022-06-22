import configparser

from abc import ABC, abstractmethod


class ConfigFileBase(ABC):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def get_value(self, main_section_name, sub_section_name, *args, **kwargs):
        pass

    @abstractmethod
    def update_val(self, main_section_name, sub_section_name, new_val, *args, **kwargs):
        pass

    @abstractmethod
    def delete_val(self, main_section_name, sub_section_name, *args, **kwargs):
        pass


class CFGFileProcessor(ConfigFileBase):
    def __init__(self, path):
        super(CFGFileProcessor, self).__init__(path)
        self.config = configparser.RawConfigParser()
        self.config.read(self.path)
        self.config.optionxform = lambda option: option

    def get_value(self, main_section_name, sub_section_name, *args, **kwargs):
        if main_section_name not in [None, ''] and sub_section_name not in [None, '']:
            if main_section_name in self.config:
                try:
                    return self.config.get(main_section_name, sub_section_name)
                except configparser.NoOptionError:
                    return
            else:
                return
        else:
            return

    def update_val(self, main_section_name, sub_section_name, new_val, *args, **kwargs):
        if any(not isinstance(x, str) for x in [main_section_name, sub_section_name, new_val]):
            raise TypeError('At least 1 variable is not string')

        if main_section_name not in self.config:
            self.config.add_section(main_section_name)
        self.config.set(main_section_name, sub_section_name, new_val)

        config_file = open(self.path, 'w')
        self.config.write(config_file)
        config_file.close()

    def delete_val(self, main_section_name, sub_section_name, *args, **kwargs):
        if main_section_name in [None, ''] or \
                main_section_name not in self.config:
            raise ValueError('first section cannot be None or "" or first section not in config file!')

        if sub_section_name not in [None, '']:
            self.config[main_section_name].pop(sub_section_name)
        else:
            self.config.pop(main_section_name)

        config_file = open(self.path, 'w')
        self.config.write(config_file)
        config_file.close()


if __name__ == '__main__':
    file_path = './config.cfg'
    test_model = CFGFileProcessor(file_path)
    m_key = ['TEST1', 'TEST3']
    s_key = ['test1', 'test3']
    value = ['100', '200']

    # for m, s, v in zip(m_key, s_key, value):
    #     print(test_model.get_value(m,s))
    #     # te new data or renew keys that included in config file
    #     test_model.update_val(m, s, v)

    m_k1='TEST1'
    s_k1='test1'

    m_k2='TEST3'
    s_k2=''

    test_model.delete_val(m_k1,s_k1)
    test_model.delete_val(m_k2,s_k2)