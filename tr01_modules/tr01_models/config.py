import os
from tr01_config import ConfigDev, ConfigProd, ConfigLocal

if os.environ.get('CONFIG_TYPE')=='local':
    config = ConfigLocal()
    print('- tr01_models/config: Local')
elif os.environ.get('CONFIG_TYPE')=='dev':
    config = ConfigDev()
    print('- tr01_models/config: Development')
elif os.environ.get('CONFIG_TYPE')=='prod':
    config = ConfigProd()
    print('- tr01_models/config: Production')