import logging

import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    logger.info(event)
    logger.info(context)

    logger.info(f'pandas version is {pd.__version__}')

    return {'pandas': pd.__version__}
