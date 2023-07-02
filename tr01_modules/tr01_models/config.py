import os
from tr01_config import ConfigDev, ConfigProd, ConfigLocal

if os.environ.get('FLASK_ENV')=='local':
    config = ConfigLocal()
    print('- tr01_models/config: Local')
elif os.environ.get('FLASK_ENV')=='dev':
    config = ConfigDev()
    print('- tr01_models/config: Development')
elif os.environ.get('FLASK_ENV')=='prod':
    config = ConfigProd()
    print('- tr01_models/config: Production')