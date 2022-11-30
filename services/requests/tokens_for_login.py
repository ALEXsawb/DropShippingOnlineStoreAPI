import os

from decouple import config

token = os.environ.get('STORE_TOKEN', config('STORE_TOKEN'))
