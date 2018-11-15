import logging
import os

import pandas as pd
from sshtunnel import create_logger, SSHTunnelForwarder, HandlerSSHTunnelForwarderError


SSH_CERTIFICATE = os.environ['SSH_CERTIFICATE']
SSH_HOSTNAME = os.environ.get['SSH_HOSTNAME']  # 'ec2-##-###-##-##.eu-west-1.compute.amazonaws.com'

MYSQL_BIND_PORT = 11000
REDSHIFT_BIND_PORT = 11004

MYSQL_ENGINE = f'mysql+pymysql://username:password@127.0.0.1:{MYSQL_BIND_PORT}/database'
REDSHIFT_ENGINE = f'postgresql://username:password@127.0.0.1:{REDSHIFT_BIND_PORT}/database'

PRODUCTION_ENGINE = MYSQL_ENGINE


def run_query(query, db_engine=PRODUCTION_ENGINE, **kwargs):

    remote_bind_address = tuple()
    local_bind_port = None

    if 'mysql' in db_engine:
        remote_bind_address = ('mysql-db-endpoint', 3306)
        local_bind_port = MYSQL_BIND_PORT
    elif 'postgresql' in db_engine:
        remote_bind_address = ('redshift-db-endpoint', 5439)
        local_bind_port = REDSHIFT_BIND_PORT

    # Create SSH tunnel
    server = None

    server_kwargs = {
        'ssh_address_or_host': SSH_HOSTNAME,
        'ssh_username': 'ec2-user',
        'ssh_pkey': SSH_CERTIFICATE,  # path
        'remote_bind_address': remote_bind_address,
        'local_bind_address': ('127.0.0.1', local_bind_port),
        'logger': create_logger(loglevel=logging.CRITICAL)
    }

    try:
        server = SSHTunnelForwarder(**server_kwargs)
        server.start()
    except HandlerSSHTunnelForwarderError:  # SSH tunnel already opened in a separate process
        server.stop()

    df = pd.read_sql_query(query, db_engine, **kwargs)

    # Close SSH tunnel
    if server:
        server.stop()

    return df
