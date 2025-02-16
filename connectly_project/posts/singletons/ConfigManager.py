# class ConfigManager:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(ConfigManager, cls).__new__(cls)
#             cls._instance.config_data = {}
#         return cls._instance
    
#     def set_config(self, key, value):
#         self.config_data[key] = value

#     def get_config(self, key, default = None):
#         return self.config_data.key(key, default)

class ConfigManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance
    

    def _initialize(self):
        self.settings = {
            "DEFAULT_PAGE_SIZE": 20,
            "ENABLE_ANALYTICS": True,
            "RATE_LIMIT": 100
        }

    def get_setting(self, key):
        return self.settings.get(key)
    
    def set_setting(self, key, value):
        self.settings[key] = value