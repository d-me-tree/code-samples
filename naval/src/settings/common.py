import os

ENV_NAME = 'common'
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '..', '..'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['root-logger'],
    },
    'formatters': {
        'root': {
            'format': '%(levelname)s:root:%(message)s',
        },
        'mario': {
            'format': '[%(levelname)s] mario %(message)s',
        }
    },
    'handlers': {
        'root-logger': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'root',
        },
        'mario': {
            'class': 'logging.StreamHandler',
            'formatter': 'mario',
        }
    },
    'loggers': {
        'mario': {
            'handlers': ['mario'],
            'level': 'INFO',
        }
    }
}
