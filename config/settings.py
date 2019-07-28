from .env_variables import SERVER
from .constant import *

# Check for development then route to respective database and configurations
server = SERVER.lower()

if SERVER.lower() in ('prod', 'production',):
    from .production import *
else:
    from .development import *

print('---------- Server in %s ----------' % SERVER)
