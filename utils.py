import json
import logging
import os
from datetime import datetime

class Config:
    """Менеджер конфигурации проекта"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        config_path = "config/settings.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки конфига: {e}")
            self.data = {}
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

class Logger:
    """Логгер для записи событий"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        config = Config()
        os.makedirs('logs', exist_ok=True)
        
        log_file = config.get('logging.log_file', 'logs/snoser.log')
        log_level = config.get('logging.log_level', 'INFO')
        log_format = config.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        self.logger = logging.getLogger('SNOSER')
        self.logger.setLevel(getattr(logging, log_level))
        
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file, encoding='utf-8')
            fh.setLevel(getattr(logging, log_level))
            formatter = logging.Formatter(log_format)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)

class DataManager:
    """Менеджер для работы с JSON-данными"""
    
    @staticmethod
    def save_senders(senders_dict, filename=None):
        config = Config()
        os.makedirs('data', exist_ok=True)
        
        if filename is None:
            filename = config.get('data_storage.senders_file', 'data/senders.json')
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(senders_dict, f, indent=2, ensure_ascii=False)
            Logger().info(f"Сохранено {len(senders_dict)} отправителей в {filename}")
            return True
        except Exception as e:
            Logger().error(f"Ошибка сохранения senders: {e}")
            return False
    
    @staticmethod
    def load_senders(filename=None):
        config = Config()
        if filename is None:
            filename = config.get('data_storage.senders_file', 'data/senders.json')
        
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            Logger().error(f"Ошибка загрузки senders: {e}")
            return {}
    
    @staticmethod
    def save_report(report_data, filename=None):
        config = Config()
        os.makedirs('data', exist_ok=True)
        
        if filename is None:
            filename = config.get('data_storage.reports_file', 'data/reports.json')
        
        try:
            reports = []
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    reports = json.load(f)
            
            report_entry = {
                'timestamp': datetime.now().isoformat(),
                'data': report_data
            }
            reports.append(report_entry)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(reports, f, indent=2, ensure_ascii=False)
            
            Logger().info(f"Отчёт сохранён в {filename}")
            return True
        except Exception as e:
            Logger().error(f"Ошибка сохранения отчёта: {e}")
            return False
