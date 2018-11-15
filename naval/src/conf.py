import importlib
import os

__all__ = ['settings']

settings = None


def initialize_settings():
    global settings

    if settings is None:
        path = os.environ.get('NAVAL_SETTINGS_MODULE') or 'settings.local'
        settings_ = importlib.import_module(path)

        if settings_.LOGGING:
            import logging.config
            logging.config.dictConfig(settings_.LOGGING)

        settings = settings_

initialize_settings()
