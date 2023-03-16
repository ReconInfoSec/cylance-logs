import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    APP_ID=os.environ.get('APP_ID')
    APP_SECRET=os.environ.get('APP_SECRET')
    TENANT_ID=os.environ.get('TENANT_ID')
    LOG_FILE='/var/log/cylance-protect.log'
