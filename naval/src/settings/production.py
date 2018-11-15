from boto3 import Session
# noinspection PyUnresolvedReferences
from settings.common import *

ENV_NAME = 'production'

boto3_session = Session()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['watchtower'],
    },
    'formatters': {
        'aws': {
            'format': '[%(levelname)s] func=%(funcName)s %(message)s',
        }
    },
    'handlers': {
        'watchtower': {
            'level': 'INFO',
            'class': 'watchtower.CloudWatchLogHandler',
                     'boto3_session': boto3_session,
                     'log_group': 'mario',
            'formatter': 'aws',
        }
    },
}
